import retrieve_info


from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/info/<genre>/<year>/<artist>', methods=['GET'])
def index(genre, year, artist):
	json_info = jsonify(retrieve_info(genre))
	# json_info = jsonify({'genre': genre
	return json_info