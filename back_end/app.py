from flask import Flask, jsonify
from flask_cors import CORS

from retrieve_info import retrieve_info

app = Flask(__name__)
CORS(app)


@app.route('/info/<genre>/<year>/<artist>', methods=['GET'])
def index(genre, year, artist):
    json_info = jsonify(retrieve_info(genre, year, artist))
    '''
    json_info = jsonify({
        'genre': genre,
        'year': year,
        'artist': artist,
    })
    '''
    return json_info
