import pandas as pd

definitions = pd.read_csv("app/data/spotify_definitions.csv", sep = ";", header =0)
data = pd.read_csv("app/data/data.csv", sep=",")

filter_columns = ["valence", "instrumentalness", "acousticness", "danceability",
                  "energy", "liveness", "loudness", "mode", "name"]
song_datas = data.filter(items=filter_columns)
# print(song_head)
