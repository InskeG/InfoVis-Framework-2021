from flask import render_template, request, jsonify
import os, json

from decimal import Decimal

import pandas as pd
import numpy as np

from app import models, data
from . import main


@main.route('/', methods=['GET'])
def index():
    home_data = data.home_data
    artists = data.top_artists
    song_data = dict(zip(artists, home_data))
    artists = json.loads(artists.to_json(orient="values"))

    return render_template("home.html", song_data=song_data, artists=artists)

# @main.route('/d3', methods = ['GET'])
# def d3():
#     mj_data = data.song_data
#     mj_json = json.loads(mj_data.to_json(orient="index"))
#     names = json.loads(data.song_names.to_json(orient="values"))
#
#     return render_template("d3.html", song_data=mj_json, names=names)
#
#
# @main.route('/d3_plot_data', methods = ['GET'])
# def d3_plot_data():
#     mj_data = data.song_data
#     mj_valence = mj_data.filter(items=["valence", "name"])
#     mj_json = json.loads(mj_valence.to_json(orient="records"))
#     print(mj_json)
#     return jsonify(mj_json)

@main.route('/metrics', methods=['GET'])
def metrics():
    song_data = data.song_data
    keys = data.filter_columns
    artists = data.top_artists

    temp_data = song_data.query("artists in @artists").sort_values("popularity", 0, False).groupby("artists").head(10)

    temp_data = temp_data.groupby("artists")
    metrics_data = {x[0] : x[1].filter(items=keys).to_dict("records") for x in temp_data}
    artists = json.loads(artists.to_json(orient="records"))

    return render_template("metrics.html", song_data=metrics_data, artists=artists, keys=keys)

@main.route('/metrics_data', methods=['GET'])
def metrics_data():
    song_data = data.song_data
    artist = request.args.get("artist")
    keys = data.filter_columns
    print(data.filtered_artists)
    print(artist)
    if artist not in data.filtered_artists:
        print("Artist not found")
        return {}

    metrics_data = song_data.query("artists == @artist").sort_values("popularity", 0, False).head(10)
    metrics_data = {artist: metrics_data.filter(items=keys).to_dict("records")}
    print(metrics_data)

    return metrics_data


@main.route('/popularity', methods=['GET'])
def popularity():
	return render_template("popularity.html")
