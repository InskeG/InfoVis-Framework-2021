from flask import render_template, request, jsonify
import os, json

from decimal import Decimal

import pandas as pd
import numpy as np

from app import models, data
from . import main


@main.route('/', methods=['GET'])
def index():
    return render_template("home.html")

@main.route('/d3', methods = ['GET'])
def d3():
    mj_data = data.mj_songs
    mj_json = json.loads(mj_data.to_json(orient="index"))
    names = json.loads(data.song_names.to_json(orient="values"))

    return render_template("d3.html", song_data=mj_json, names=names)


@main.route('/d3_plot_data', methods = ['GET'])
def d3_plot_data():
    mj_data = data.mj_songs
    mj_valence = mj_data.filter(items=["valence", "name"])
    mj_json = json.loads(mj_valence.to_json(orient="records"))
    print(mj_json)
    return jsonify(mj_json)

@main.route('/metrics', methods=['GET'])
def metrics():
	return render_template("metrics.html")

@main.route('/popularity', methods=['GET'])
def popularity():
	return render_template("popularity.html")
