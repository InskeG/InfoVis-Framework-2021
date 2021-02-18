from flask import Flask, jsonify
from flask_cors import CORS

from retrieve_info import retrieve_info

app = Flask(__name__)
CORS(app)


@app.route('/info/<genre>/<year>', methods=['GET'])
def index(genre, year):
    json_info = jsonify(retrieve_info(genre, year))
    '''
    json_info = jsonify({
        'genre': genre,
        'year': year
        'summary': summary,
        'related_terms': terms,
    })
    '''
    return json_info
