import binascii
import numpy as np
import os
import scipy
import scipy.misc
import scipy.cluster
import struct

from flask import Flask, jsonify
from flask_cors import CORS
from PIL import Image

from retrieve_info import retrieve_info

NUM_CLUSTERS = 5
RESIZE = 150

app = Flask(__name__)
CORS(app)


def detect_colors(image):

    image = image.resize((RESIZE, RESIZE))      # optional, to reduce time
    array = np.asarray(image)
    shape = array.shape
    array = array.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    codes, dist = scipy.cluster.vq.kmeans(array, NUM_CLUSTERS)
    print('cluster centres:\n', codes)

    vecs, dist = scipy.cluster.vq.vq(array, codes)         # assign codes
    counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

    index_max = scipy.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    color = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    print('most frequent is %s (#%s)' % (peak, color))

    return f"#{color}"


@app.route('/info/<genre>/<year>', methods=['GET'])
def index(genre, year):
    info = retrieve_info(genre, year)

    path = os.path.join(os.path.dirname(__file__), "img1.jpg")
    image = Image.open(path)
    color = detect_colors(image)
    info['color'] = color
    print(info)

    json_info = jsonify(info)
    '''
    json_info = jsonify({
        'genre': genre,
        'year': year
        'summary': summary,
        'related_terms': terms,
    })
    '''

    return json_info
