import retrieve_info

from flask import Flask, jsonify
app = Flask(__name__)

# for example: http://127.0.0.1:5000/info/Post-impressionism/1943/vincent+van+gogh
@app.route('/info/<genre>/<year>/<artist>', methods=['GET'])
def index(genre, year, artist):
	# json_info = jsonify(retrieve_info(genre))
	json_info = jsonify({'genre': genre,
	'year': year,
	'artist': artist})
	return json_info