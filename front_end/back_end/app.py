from retrieve_info import retrieve_info

from flask import Flask, jsonify
app = Flask(__name__)

# for example: http://127.0.0.1:5000/info/impressionism/1954/vincent%20van%20gogh
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
