import binascii
import numpy as np
import os
import scipy
import scipy.misc
import scipy.cluster
import time

from base64 import encodebytes
from io import BytesIO
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from PIL import Image
import pandas as pd
# from data import *

# from retrieve_info import retrieve_info

# model_data = get_model_data()

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


def get_model_data():
    stats_art = pd.read_csv('./data/omniart_v3_datadump.csv')
    model_data = stats_art.copy()[:30]
    # model_data = model_data.drop(model_data[model_data['artist_full_name'] == 'unknown'] and model_data[model_data['creation_year'] == 'unknown'].index)
    model_data = model_data.drop(model_data[model_data['artist_full_name'] == 'unknown'].index)
    model_data = model_data.drop(model_data[model_data['creation_year'] == 'unknown'].index)
    return model_data

def stripp(x):
    return x.strip(' ')

def get_artists(model_data):
    all_artist_text = sorted(model_data['artist_full_name'].astype(str).unique().tolist())
    # art_list = [x.strip(' ') for x in all_artist_text]
    art_list = list(map(stripp, all_artist_text))
    # art_list = []
    # for x in all_artist_text:
    #     art_list.append({'text': x.strip(' ')})

    return art_list


def get_line_chart(model_data):
    # stats_art = pd.read_csv('./data/omniart_v3_datadump.csv')
    # model_data = stats_art.copy()
    # # model_data = model_data.drop(model_data[model_data['artist_full_name'] == 'unknown'] and model_data[model_data['creation_year'] == 'unknown'].index)
    # model_data = model_data.drop(model_data[model_data['artist_full_name'] == 'unknown'].index)
    # model_data = model_data.drop(model_data[model_data['creation_year'] == 'unknown'].index)
    line_graph = {}

    a = model_data['creation_year'].tolist()
    b = model_data['dominant_color'].tolist()
    c = model_data['artist_full_name'].tolist()
    
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


# @app.route('/info/<genre>/<year>', methods=['GET'])
# def index(genre, year):
#     # info = retrieve_info(genre, year)
#     info = {}

#     # Load a placeholder image.
#     # TODO: Obtain a generated image here.
#     path = os.path.join(os.path.dirname(__file__), "img4.jpg")
#     image = Image.open(path)

#     # Encode the image for the response.
#     img_stream = BytesIO()
#     image.save(img_stream, format="png")
#     encoded_img = encodebytes(img_stream.getvalue()).decode('ascii')
#     info['image'] = f"data:image/png;base64, {encoded_img}"

#     # Get the primary color of the image.
#     colors, percentages, dom_color = detect_colors(image)
#     info['colors'] = colors
#     info['percentages'] = percentages
#     info['dom_color'] = dom_color

#     json_info = jsonify(info)

#     return json_info



# @app.route('/line_chart', methods=['GET'])
# def artist_options(artist):
#     # info = retrieve_info(genre, year)
#     line = {}

#     model_data = get_model_data()

#     line_graph, serie = get_artists(model_data)
#     # Get the primary color of the image.
#     line['dicti'] = line_graph
#     line['serie'] = serie
    
#     json_info = jsonify(line)

#     return json_info

# @app.route('/line_chart/<artist>', methods=['GET'])
# def line_chart(artist):
#     # info = retrieve_info(genre, year)
#     line = {}

#     line_graph, serie = get_line_graph(model_data)
#     # Get the primary color of the image.
#     line['dicti'] = line_graph
#     line['serie'] = serie
    
#     json_info = jsonify(line)

#     return json_info


@socketio.event
def collect_info(data):

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

    model_data = get_model_data()


    selected_artist = get_artists(model_data)

    socketio.emit("set_selected_artist", {
        "artist_options": selected_artist,
    })


    series = get_line_chart(model_data)

    socketio.emit("line_chart", {
        "series": series,
    })







@socketio.on('connect')
def test_connect():
    print("Connected")


if __name__ == "__main__":
    socketio.run(app)
