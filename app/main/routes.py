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
    artists = data.artists
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
    metrics_data = data.metrics_data
    keys = data.filter_columns
    artists = data.metrics_artists
    colors = data.heatmap_colors
    # negatived = [{k:(v * -1) for (k, v) in x.items()} for x in records]
    # records = [[x, y] for x,y in zip(records, negatived)]
    # print(records)
    artists = json.loads(artists.to_json(orient="records"))
    colors = dict(zip(colors["characteristic"], colors.filter(items=["color_min", "color_max"]).to_dict(orient="records")))
    print(colors)

    return render_template("metrics.html", song_data=metrics_data, artists=artists, keys=keys, colors=colors)

@main.route('/popularity', methods=['GET'])
def popularity():
	return render_template("popularity.html")
