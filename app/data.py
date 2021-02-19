import pandas as pd
import numpy as np
import ast

definitions = pd.read_csv("app/data/spotify_definitions.csv", sep = ";", header =0)
data = pd.read_csv("app/data/data_by_artist.csv", sep=",")

filter_home_page = ["popularity", "artists"]
home_data = data.filter(items=filter_home_page)
home_data = home_data.sort_values("popularity", 0, False).head(10)

print(dict(zip(home_data["artists"], home_data["popularity"])))

filter_columns = ["valence", "instrumentalness", "acousticness", "danceability",
                  "energy", "liveness", "loudness", "mode", "artists"]
song_data = data.filter(items=filter_columns)
song_head = song_data.head(20)
