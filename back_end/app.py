import binascii
import json
import numpy as np
import os
import pandas as pd
import pickle
import scipy
import sys
import torch
import wikipedia

from base64 import encodebytes
from colour import Color
from io import BytesIO
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from io import BytesIO
from PIL import Image
from scipy import cluster

from .retrieve_info import retrieve_info, _get_artist_histograms
from .data import model_data, all_artists, _get_timeline_data
from .GAN import dnnlib, generate

sys.path.append("./GAN/")

if torch.cuda.is_available():
    DEVICE = torch.device('cuda')

    with dnnlib.util.open_url("./GAN/models/artists.pkl") as f:
        G_artists = pickle.Unpickler(f).load()['G_ema'].to(DEVICE)

    with dnnlib.util.open_url("./GAN/models/centuries.pkl") as f:
        G_centuries = pickle.Unpickler(f).load()['G_ema'].to(DEVICE)

NUM_CLUSTERS = 4
RESIZE = 150  # Size of images for clustering.


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')


def detect_colors(image):
    image = image.resize((RESIZE, RESIZE))

    array = np.asarray(image)
    shape = array.shape
    array = array.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    codes, dist = cluster.vq.kmeans(array, NUM_CLUSTERS)

    vecs, dist = cluster.vq.vq(array, codes)
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

    year_list = pd.Series.tolist(year_df['artwork_name'])
    if len(year_list) < 5:
        dictionary['same_year/genre'] = pd.Series.tolist(year_df['artwork_name'])
    else:
        dictionary['same_year/genre'] = pd.Series.tolist(year_df['artwork_name'])[:5]

    dictionary['related_terms'] = wikipedia.search(genre)

    # other = model_data.loc[model_data['artist_full_name'] == artist]

    return dictionary


def get_artists(model_data):
    all_artist_text = sorted(model_data['school'].astype(str).unique().tolist())

    return all_artist_text


def get_line_chart(model_data):
    line_graph = {}

    a = model_data['creation_year'].tolist()
    b = model_data['dominant_color'].tolist()
    labels = model_data['school'].tolist()

    for i, artist in enumerate(labels):
        if artist not in line_graph.keys():
            line_graph[artist] = []
        line_graph[artist].append([a[i], b[i]])

    serie = []
    for artist in line_graph.keys():
        serie.append({
            'values': line_graph[artist],
            'text': artist
        })
    return serie


def get_line_chart_artist(model_data, label):
    """
    Collect data for the school/dominant color linechart.
    """
    series = []

    data = model_data[model_data.artist_last_name == label]
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

        values.append((int(eval(year)), hue))
        styles.append(color.hex)

    series.append({
        # 'styles': styles,
        'text': label,
        'values': values,
    })

    data = {
        'series': series,
        'plot': {
            'marker': {
                'styles': [
                    {'background-color': color} for color in styles
                ],
            },
        },
    }

    return data


def encode_image(image, format='png'):
    """
    Encode an image into base64 so it can be send along with an event.

    Parameters
    ----------
    image: PIL.Image
    format: str, default 'png'
    """
    stream = BytesIO()
    image.save(stream, format=format)
    encoded = encodebytes(stream.getvalue()).decode('ascii')

    return f"data:image/{format};base64, {encoded}"


@socketio.event
def collect_line_chart(data):
    data = get_line_chart_artist(model_data, data['artist'])
    print("Collecting line chart data", data)
    socketio.emit("collect_line_chart", data)


@socketio.event
def collect_info(data):
    print("Hallo, ik kom hier om dingen volledig in de war te gooien!")
    gen = data['genre']
    y = data['year']

    # Load a placeholder image.
    # TODO: Obtain a generated image here.
    image_file = {
        "Impressionism": "img1.jpg",
        "Expressionism (fine arts)": "img2.jpg",
        "Cubism": "img3.jpg",
        "Surrealism": "img4.jpg",
    }.get(gen, "img1.jpg")
    path = os.path.join(os.path.dirname(__file__), image_file)
    image = Image.open(path)

    # Encode the image for the response.
    img_stream = BytesIO()
    image.save(img_stream, format="png")
    encoded_img = encodebytes(img_stream.getvalue()).decode('ascii')

    socketio.emit("set_image", {
        "existend": f"data:image/png;base64, {encoded_img}",
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

    socketio.emit("get_summary", {
        "summary": dictionary['summary'],
        "related_terms": dictionary['related_terms']
    })

    socketio.emit("set_selected_artist", {
        "artist_options": get_artists(model_data),
    })

    # socketio.emit("line_chart", {
    #     "series": get_line_chart(model_data),
    # })

    '''
    histograms = get_artist_histograms()
    socketio.emit("get_style_hists", {
        "series": [{
            "values": values,
            "text": key,
        } for key, values in histograms.items()],
    })
    '''


@socketio.event
def generate_images(data):
    if not torch.cuda.is_available():
        socketio.emit("images_generated", {
            "images": [],
            "seeds": [],
            "success": False,
            "message": "No Graphical Processing Unit available!"
        })
        return

    classification_type = data["type"]
    amount = data["amount"]
    class_idx = data["class_idx"]

    seeds = np.random.randint(0, 10000, amount)

    if classification_type == "artists":
        try:
            class_idx = generate.ARTIST_LABELS.index(class_idx)
        except ValueError:
            message = f"Label {repr(class_idx)} does not exist!"
            socketio.emit("images_generated", {
                "images": [],
                "seeds": [],
                "success": False,
                "message": message,
            })
            raise ValueError(message)

        images = generate.generate_images(G_artists, seeds, class_idx)
    elif classification_type == "centuries":
        print(f"Generating painting from the {class_idx}th century")
        images = generate.generate_images(G_centuries, seeds, class_idx)
    else:
        message = f"Type {repr(classification_type)} is not known!"
        socketio.emit("images_generated", {
            "images": [],
            "seeds": [],
            "success": False,
            "message": message
        })
        raise ValueError(message)

    image_data = []

    for image in images:
        colors, percentages, dom_color = detect_colors(image)

        image_data.append({
            'image': encode_image(image),
            'dominant_color': dom_color,
            'color_palette': colors,
            'color_distribution': percentages,
        })

    first_image = image_data[0]
    socketio.emit("change_color", first_image['dominant_color'])
    socketio.emit("set_color_pie", {
        "colors": first_image['color_palette'],
        "percentages": first_image['color_distribution'],
    })

    socketio.emit("images_generated", {
        "images": image_data,
        "seeds": seeds.tolist(),
        "success": True,
        "message": ""
    })


@socketio.event
def get_timeline_data(artists=None, adding=False):
    timeline_data, artists = _get_timeline_data(artists, adding)
    return {
        'timelineData': timeline_data,
        'artists': artists
    }


@socketio.event
def get_all_artists():
    return all_artists


@socketio.event
def get_artist_histograms(data):
    artists = data['artists']
    print(artists)
    histograms = _get_artist_histograms(artists)
    socketio.emit("get_style_hists", {
        "series": [{
            "values": values,
            "text": key,
        } for key, values in histograms.items()],
    })


@socketio.on('connect')
def test_connect():
    print("Connected")


if __name__ == "__main__":
    socketio.run(app)
