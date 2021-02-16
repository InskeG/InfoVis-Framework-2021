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
    plot_data = data.song_datas
    plot_head = plot_data.head(1)
    plot_head = json.loads(plot_head.to_json())
    print(plot_head["name"])

    return render_template("d3.html", song_data=plot_head)


@main.route('/d3_plot_data', methods = ['GET'])
def d3_plot_data():
    plot_data = data.song_datas
    plot_head = plot_data.head(20)
    plot_head = plot_head.to_json()
    return plot_head
