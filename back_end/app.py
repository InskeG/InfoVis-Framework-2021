import binascii
import numpy as np
import os
import scipy
import scipy.misc
import scipy.cluster
import time

from base64 import encodebytes
from colour import Color
from io import BytesIO
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from PIL import Image
import pandas as pd
import wikipedia

# StyleGan imports
import sys
sys.path.append("./GAN/")

from .GAN import dnnlib
from .GAN import generate
from .retrieve_info import retrieve_info, get_style_histograms
import pickle
import torch


if torch.cuda.is_available():
    DEVICE = torch.device('cuda')

    with dnnlib.util.open_url("./GAN/models/artists.pkl") as f:
        G_artists = pickle.Unpickler(f).load()['G_ema'].to(DEVICE)

    with dnnlib.util.open_url("./GAN/models/centuries.pkl") as f:
        G_centuries = pickle.Unpickler(f).load()['G_ema'].to(DEVICE)

nr_color = 3
NUM_CLUSTERS = 4
RESIZE = 150


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')


def detect_colors(image):
    image = image.resize((RESIZE, RESIZE))

    array = np.asarray(image)
    shape = array.shape
    array = array.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    codes, dist = scipy.cluster.vq.kmeans(array, NUM_CLUSTERS)

    vecs, dist = scipy.cluster.vq.vq(array, codes)
    counts, bins = scipy.histogram(vecs, len(codes))

    total = np.sum(np.array(counts))
    percentages = (counts / total)

    color_list = []
    for code in codes:
        hex_color = binascii.hexlify(bytearray(
            int(c) for c in code
        )).decode('ascii')
        color_list.append(f"#{hex_color}")

    dom_code = codes[scipy.argmax(counts)]
    dom_hex = binascii.hexlify(bytearray(
        int(c) for c in dom_code
    )).decode('ascii')
    dom_color = f"#{dom_hex}"

    colors = color_list

    return list(colors), list(percentages), dom_color


def retrieve_info(genre, year, model_data):
    year = float(year)
    ranges = float(1)
    dictionary = {}

    w = wikipedia.page(genre)
    dictionary['genre'] = w.title

    dictionary['summary'] = wikipedia.summary(genre, sentences=3)


    # print('artworks in same time period:')
    # other art pieces created in same year
    year_df = model_data.loc[model_data['creation_year'].astype('float') < year+ranges]
    year_df = year_df.loc[year_df['creation_year'].astype('float') > year-ranges]

    # print(year_df)
    year_list = pd.Series.tolist(year_df['artwork_name'])
    if len(year_list) < 5:
        dictionary['same_year/genre'] = pd.Series.tolist(year_df['artwork_name'])
    else:
        dictionary['same_year/genre'] = pd.Series.tolist(year_df['artwork_name'])[:5]

    dictionary['related_terms'] = wikipedia.search(genre)

    # other = model_data.loc[model_data['artist_full_name'] == artist]

    return dictionary


def get_model_data():
    stats_art = pd.read_csv('./data/omniart_v3_datadump.csv')
    model_data = stats_art.copy()[:100]
    model_data = model_data.drop(model_data[model_data['school'] == 'unknown'].index)
    model_data = model_data.drop(model_data[model_data['creation_year'] == 'unknown'].index)
    return model_data


model_data = get_model_data()


def stripp(x):
    return x.strip(' ')


def get_artists(model_data):
    all_artist_text = sorted(model_data['school'].astype(str).unique().tolist())
    # art_list = list(map(stripp, all_artist_text))

    return all_artist_text


def get_line_chart(model_data):
    line_graph = {}

    a = model_data['creation_year'].tolist()
    b = model_data['dominant_color'].tolist()
    c = model_data['school'].tolist()

    labels = c

    for i, artist in enumerate(c):
        if artist not in line_graph.keys():
            line_graph[artist] = []
        line_graph[artist].append([a[i], b[i]])

    serie = []
    for artist in line_graph.keys():
        serie.append( {
            'values': line_graph[artist],
            'text': artist
        }
        )
    return serie


def get_line_chart_artist(model_data, label):
    """
    Collect data for the school/dominant color linechart.
    """
    series = []

    data = model_data[model_data.school == label]
    data = data[['creation_year', 'dominant_color']]
    data = data.sort_values(by='creation_year')
    data['hue'] = [Color(color).hue for color in data.dominant_color]

    values = []
    styles = []

    # For years with more than one work that year, we take the average
    # hue of all the dominant colors in that year.
    for year in data.creation_year.unique():
        hue = data[data.creation_year == year].hue.mean()
        color = Color(hue=hue, saturation=1, luminance=0.5)

        values.append((year, hue))
        styles.append(color.hex)

    series.append({
        'marker': {'visible': False},
        'styles': styles,
        'text': label,
        'values': values,
    })

    return series


@socketio.event
def collect_line_chart(data):
    series = get_line_chart_artist(model_data, data['artist'])
    socketio.emit("collect_line_chart", {
        "series": series,
    })


@socketio.event
def collect_info(data):
    gen = data['genre']
    y = data['year']

    # Load a placeholder image.
    # TODO: Obtain a generated image here.
    path = os.path.join(os.path.dirname(__file__), "img1.jpg")
    image = Image.open(path)

    # Encode the image for the response.
    img_stream = BytesIO()
    image.save(img_stream, format="png")
    encoded_img = encodebytes(img_stream.getvalue()).decode('ascii')

    socketio.emit("set_image", {
        "generated": f"data:image/png;base64, {encoded_img}",
    })

    # Get the primary color of the image.
    colors, percentages, dom_color = detect_colors(image)

    socketio.emit("change_color", dom_color)

    socketio.emit("set_color_pie", {
        "colors": colors,
        "percentages": percentages,
    })

    # model_data = get_model_data()

    dictionary = retrieve_info(gen, y, model_data)

    print(dictionary.keys())
    socketio.emit("get_summary", {
        "summary": dictionary['summary'],
        "related_terms": dictionary['related_terms']
    })


    selected_artist = get_artists(model_data)

    socketio.emit("set_selected_artist", {
        "artist_options": selected_artist,
    })


    series = get_line_chart(model_data)

    socketio.emit("line_chart", {
        "series": series,
    })


@socketio.event
def generate_images(data):
    if not torch.cuda.is_available():
        socketio.emit("images_generated", {
            "images": [],
            "seeds": [],
            "message": "No Graphical Processing Unit available!"
        })
        return

    classification_type = data["type"]
    amount = data["amount"]
    class_idx = data["class_idx"]

    seeds = np.random.randint(0, 10000, amount)

    images = []
    if classification_type == "artists":
        images = generate.generate_images(G_artists, seeds, class_idx)
    elif classification_type == "centuries":
        images = generate.generate_images(G_centuries, seeds, class_idx)

    socketio.emit("images_generated", {
        "images": images,
        "seeds": seeds.tolist(),
        "message": ""
    })

    socketio.emit("get_style_hists", get_style_histograms())


@socketio.on('connect')
def test_connect():
    print("Connected")


if __name__ == "__main__":
    socketio.run(app)
