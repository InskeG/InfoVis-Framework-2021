import scipy
import binascii
import numpy as np
import os
from base64 import encodebytes
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from io import BytesIO
from PIL import Image

import data

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


@app.route('/info/<genre>/<year>', methods=['GET'])
def index(genre, year):
    # info = retrieve_info(genre, year)
    info = {}

    # Load a placeholder image.
    # TODO: Obtain a generated image here.
    path = os.path.join(os.path.dirname(__file__), "img2.jpg")
    image = Image.open(path)

    # Encode the image for the response.
    img_stream = BytesIO()
    image.save(img_stream, format="png")
    encoded_img = encodebytes(img_stream.getvalue()).decode('ascii')
    info['image'] = f"data:image/png;base64, {encoded_img}"

    # Get the primary color of the image.
    colors, percentages, dom_color = detect_colors(image)
    info['colors'] = colors
    info['percentages'] = percentages
    info['dom_color'] = dom_color

    json_info = jsonify(info)

    return json_info


@socketio.event
def collect_info(data):
    # Load a placeholder image.
    # TODO: Obtain a generated image here.
    path = os.path.join(os.path.dirname(__file__), "img2.jpg")
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
    socketio.emit("set_color_pie", {
        "colors": colors,
        "percentages": percentages,
    })

    socketio.emit("change_color", dom_color)


@socketio.event
def get_timeline_data():
    bla = data.get_timeline_data()
    return bla

@socketio.on('connect')
def test_connect():
    print("Connected")


if __name__ == "__main__":
    socketio.run(app)
