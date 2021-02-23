import pandas as pd
import numpy as np
import ast

definitions = pd.read_csv("app/data/spotify_definitions.csv", sep = ";", header =0)
data_by_artist = pd.read_csv("app/data/data_by_artist.csv", sep=",")
data = pd.read_csv("app/data/data.csv", sep=",")
data["artists"] = data["artists"].apply(lambda x: ast.literal_eval(x))

artist_data = data_by_artist.sort_values("popularity", 0, False).head(10)
artists = artist_data["artists"]
home_data = artist_data.popularity


filter_columns = ["valence", "acousticness", "danceability",
                  "energy", "liveness"]
# metrics_artists = pd.Series(["Michael Jackson", "Lady Gaga", "Ladytron"])
song_data = data.explode("artists")
# song_data = song_data.query("artists in @metrics_artists")
metrics_artists = song_data.groupby("artists").filter(lambda x: len(x) == 10).sample(4  )["artists"]
# metrics_artists = pd.Series(song_data["artists"].unique())
metrics_data = song_data.query("artists in @metrics_artists").groupby("artists")
metrics_data = {x[0] : x[1].filter(items=filter_columns).to_dict("records") for x in metrics_data}
# print(metrics_data)
