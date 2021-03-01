import pandas as pd
import numpy as np
import ast

# Reading in data
definitions = pd.read_csv("app/data/spotify_definitions.csv", sep = ";", header =0)
data_by_artist = pd.read_csv("app/data/data_by_artist.csv", sep=",")
data = pd.read_csv("app/data/data.csv", sep=",")
data["artists"] = data["artists"].apply(lambda x: ast.literal_eval(x))

song_data = data.explode("artists")

# Data for home page
filtered_artists = song_data.groupby("artists").filter(lambda x: len(x) > 9)["artists"]
top_artist_data = data_by_artist.query("artists in @filtered_artists").sort_values("popularity", 0, False).head(10)
top_artists = top_artist_data["artists"]
home_data = top_artist_data.popularity


# Data for metrics page
filter_columns = ["valence", "acousticness", "danceability",
                  "energy", "liveness", "speechiness", "instrumentalness",
                  "loudness", "tempo"]
metrics_data = song_data.query("artists in @top_artists").sort_values("popularity", 0, False).groupby("artists").head(10)

metrics_data["loudness"] = (metrics_data["loudness"] - min(metrics_data["loudness"]))/(
        max(metrics_data["loudness"])-min(metrics_data["loudness"]))
metrics_data["tempo"] = (metrics_data["tempo"] - min(metrics_data["tempo"]))/(
        max(metrics_data["tempo"])-min(metrics_data["tempo"]))
metrics_data = metrics_data.groupby("artists")
metrics_data = {x[0] : x[1].filter(items=filter_columns).to_dict("records") for x in metrics_data}
print(metrics_data)

heatmap_colors = pd.read_csv("app/data/heatmap_colors.csv")
