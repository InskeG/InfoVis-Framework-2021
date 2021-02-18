import pandas as pd

definitions = pd.read_csv("app/data/spotify_definitions.csv", sep = ";", header =0)
data = pd.read_csv("app/data/data.csv", sep=",")

filter_columns = ["valence", "instrumentalness", "acousticness", "danceability",
                  "energy", "liveness", "loudness", "mode", "name", "artists"]
song_data = data.filter(items=filter_columns)
mask = song_data.artists.apply(lambda x: "Michael Jackson" in x)
mj_songs = song_data[mask]
mj_songs = mj_songs.head(10)
song_names = mj_songs.filter(items=["name"])
# print(song_names)
# song_head = song_data.head(20)
# print(song_head)
