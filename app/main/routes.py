from flask import render_template, request, jsonify
import os, json

from decimal import Decimal

import pandas as pd
import numpy as np

from app import models, data
from . import main

@main.route('/', methods=['GET'])
def metrics():
    song_data = data.song_data
    keys = data.filter_columns
    keys_axis = keys[:9]
    artists = data.top_artists
    all_artists = data.filtered_artists
    heatmap_data = data.heatmap_head
    colors = data.heatmap_colors

    popularity = dict(zip(heatmap_data.artists, heatmap_data.popularity))

    heatmap_data = heatmap_data.filter(items=keys_axis + ["artists"])
    heatmap_data = pd.melt(heatmap_data, id_vars=["artists"], var_name=["characteristic"])
    heatmap_data = heatmap_data.to_dict(orient="records")

    colors = colors.to_dict(orient="records")

    barchart_data = song_data.query("artists in @artists").sort_values("popularity", 0, False).groupby("artists")
    distplot_data = pd.melt(data.distplot_data, var_name=["characteristic"])
    distplot_data  = distplot_data.to_dict(orient="records")

    #data for getting BPM in tooltips
    max_temp_art = data.max_temp_art
    min_temp_art = data.min_temp_art
    max_temp = data.max_temp
    min_temp = data.min_temp

    barchart_data = barchart_data.head(10).groupby("artists")
    barchart_data = {x[0] : x[1].filter(items=keys).to_dict("records") for x in barchart_data}

    return render_template("home.html", heatmap_data=heatmap_data,
                           heatmap_colors=colors, song_data=barchart_data,
                           artists=artists, keys=keys_axis, popularity=popularity,
                           all_artists=all_artists, max_temp_art=max_temp_art,
                           min_temp_art=min_temp_art, max_temp=max_temp,
                           min_temp=min_temp, distplot_data=distplot_data)

@main.route('/metrics_data', methods=['GET'])
def metrics_data():
    song_data = data.song_data
    heatmap_data = data.heatmap_data
    distplot_data = data.distplot_data
    artist = request.args.get("artist")
    keys = data.filter_columns
    keys_axis = keys[:9]

    if artist not in data.filtered_artists:
        print("Artist not found")
        return {}

    barchart_data = song_data.query("artists == @artist").sort_values("popularity", 0, False).head(10)
    barchart_data = {artist: barchart_data.filter(items=keys).to_dict("records")}

    artist_data = heatmap_data.query("artists == @artist")

    popularity = {artist: artist_data["popularity"].to_list()}

    heatmap_data = artist_data.filter(items=keys_axis + ["artists"])
    heatmap_data = pd.melt(heatmap_data, id_vars=["artists"], var_name=["characteristic"])
    heatmap_data = heatmap_data.to_dict(orient="records")

    return {"heatmap" : heatmap_data, "barchart": barchart_data, "popularity": popularity}

@main.route('/filter_data', methods=['GET'])
def filter_data():
    song_data = data.song_data
    keys = data.filter_columns
    keys_axis = keys[:9]
    heatmap_data = data.heatmap_data

    max_temp_art = data.max_temp_art
    min_temp_art = data.min_temp_art

    for key in keys_axis:
        min_key = float(request.args.get("min_" + key)) / 100
        max_key = float(request.args.get("max_" + key)) / 100
        queryString = "{0} >= {1} and {0} <= {2}".format(key, min_key, max_key)
        heatmap_data = heatmap_data.query(queryString)

    heatmap_data = heatmap_data.sort_values("popularity", ascending=False)
    heatmap_data = heatmap_data.head(10)

    artists = heatmap_data["artists"].to_list()

    popularity = dict(zip(heatmap_data.artists, heatmap_data.popularity))

    heatmap_data = heatmap_data.filter(items=keys_axis + ["artists"])
    heatmap_data = pd.melt(heatmap_data, id_vars=["artists"], var_name=["characteristic"])
    heatmap_data = heatmap_data.to_dict(orient="records")

    barchart_data = song_data.query("artists in @artists").sort_values("popularity", 0, False).groupby("artists")

    barchart_data = barchart_data.head(10).groupby("artists")
    barchart_data = {x[0] : x[1].filter(items=keys).to_dict("records") for x in barchart_data}

    return {"heatmap" : heatmap_data, "barchart": barchart_data, "popularity": popularity, "artists": artists}
