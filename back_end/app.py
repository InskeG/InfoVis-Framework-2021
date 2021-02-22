import binascii
import numpy as np
import os
import scipy
import scipy.misc
import scipy.cluster

from base64 import encodebytes
from io import BytesIO
from flask import Flask, jsonify
from flask_cors import CORS
from PIL import Image

from retrieve_info import retrieve_info

NUM_CLUSTERS = 5
RESIZE = 150

app = Flask(__name__)
CORS(app)


def detect_colors(image):
    image = image.resize((RESIZE, RESIZE))

    array = np.asarray(image)
    shape = array.shape
    array = array.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    codes, dist = scipy.cluster.vq.kmeans(array, NUM_CLUSTERS)

    vecs, dist = scipy.cluster.vq.vq(array, codes)
    counts, bins = scipy.histogram(vecs, len(codes))

    # Find the most prominent color.
    index_max = scipy.argmax(counts)
    peak = codes[index_max]

    # Convert the color to hex representation.
    color = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')

    return f"#{color}"


@app.route('/info/<genre>/<year>', methods=['GET'])
def index(genre, year):
    info = retrieve_info(genre, year)
    # info = {}

    # Load a placeholder image.
    # TODO: Obtain a generated image here.
    path = os.path.join(os.path.dirname(__file__), "img1.jpg")
    image = Image.open(path)

    # Encode the image for the response.
    img_stream = BytesIO()
    image.save(img_stream, format="png")
    encoded_img = encodebytes(img_stream.getvalue()).decode('ascii')
    info['image'] = f"data:image/png;base64, {encoded_img}"

    # Get the primary color of the image.
    color = detect_colors(image)
    info['color'] = color


    json_info = jsonify(info)

    return json_info
