import pandas as pd
import numpy as np
import ast

# Reading in data
definitions = pd.read_csv("app/data/spotify_definitions.csv", sep = ";", header =0)
data_by_artist = pd.read_csv("app/data/data_by_artist.csv", sep=",")
data = pd.read_csv("app/data/data.csv", sep=",")
data["artists"] = data["artists"].apply(lambda x: ast.literal_eval(x))

song_data = data.explode("artists")
max_loud = max(song_data["loudness"])
min_loud = min(song_data["loudness"])
max_temp = max(song_data["tempo"])
min_temp = min(song_data["tempo"])
song_data["loudness"] = (song_data["loudness"] - min_loud)/(
    max_loud-min_loud)
song_data["tempo"] = (song_data["tempo"] - min_temp)/(
    max_temp-min_temp)

max_loud = max(data_by_artist["loudness"])
min_loud = min(data_by_artist["loudness"])
max_temp = max(data_by_artist["tempo"])
min_temp = min(data_by_artist["tempo"])
data_by_artist["loudness"] = (data_by_artist["loudness"] - min_loud)/(
    max_loud-min_loud)
data_by_artist["tempo"] = (data_by_artist["tempo"] - min_temp)/(
    max_temp-min_temp)

# Data for home page
filtered_artists = song_data.groupby("artists").filter(lambda x: len(x) > 9)["artists"].unique().tolist()
# filtered_artists = data_by_artist.query("count>9")["artists"].to_list()
filtered_data = data_by_artist.query("artists in @filtered_artists")
filtered_data = filtered_data.set_index("artists")

top_artist_data = filtered_data.sort_values("popularity", 0, False).head(10)
top_artists = top_artist_data.index.to_list()

home_data = top_artist_data.popularity


# Data for metrics page
filter_columns = ["valence", "acousticness", "danceability",
                  "energy", "liveness", "speechiness", "instrumentalness",
                  "loudness", "tempo"]

# print(filtered_data)
# for artist in top_artists:
#     count_1 = filtered_data.at[artist, "count"]
#     count_2 = song_data.query("artists == @artist").size
#     print(count_1, count_2)

heatmap_data = data_by_artist.query("artists in @filtered_artists").sort_values("popularity", ascending=False)
heatmap_head = heatmap_data.head(10)

heatmap_colors = pd.read_csv("app/data/heatmap_colors.csv")
