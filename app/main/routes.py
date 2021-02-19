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
    song_data = dict(zip(home_data["artists"], home_data["popularity"]))
    artists = json.loads(home_data["artists"].to_json(orient="values"))

    return render_template("home.html", song_data=song_data, artists=artists)

"""@main.route('/d3', methods = ['GET'])
def d3():
    mj_data = data.song_data
    mj_json = json.loads(mj_data.to_json(orient="index"))
    names = json.loads(data.song_names.to_json(orient="values"))

    return render_template("d3.html", song_data=mj_json, names=names)


@main.route('/d3_plot_data', methods = ['GET'])
def d3_plot_data():
    mj_data = data.song_data
    mj_valence = mj_data.filter(items=["valence", "name"])
    mj_json = json.loads(mj_valence.to_json(orient="records"))
    print(mj_json)
    return jsonify(mj_json)"""

@main.route('/metrics', methods=['GET'])
def metrics():
    heatmap_data = data.heatmap_head
    #heatmap_data["loudness"] = heatmap_data["loudness_01"]
    #heatmap_data["tempo"] = heatmap_data["tempo_01"]
    heatmap_data = heatmap_data.drop(["loudness", "tempo"], 1)
    heatmap_data = pd.melt(heatmap_data, id_vars=["artists"], var_name=["characteristic"])

    return render_template("metrics.html", heatmap_data=heatmap_data.to_dict(orient='records'))

@main.route('/popularity', methods=['GET'])
def popularity():
    return render_template("popularity.html")
