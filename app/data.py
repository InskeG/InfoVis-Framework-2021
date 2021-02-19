import pandas as pd
import numpy as np
import ast

definitions = pd.read_csv("app/data/spotify_definitions.csv", sep = ";", header =0)
data = pd.read_csv("app/data/data_by_artist.csv", sep=",")

filter_home_page = ["popularity", "artists"]
home_data = data.filter(items=filter_home_page)
home_data = home_data.sort_values("popularity", 0, False).head(10)

filter_columns = ["artists", "acousticness", "danceability", "energy",
                  "instrumentalness", "liveness", "loudness", "speechiness", "tempo",
				  "valence", "popularity", "count"]
heatmap_data = data[data["count"]>9].sort_values("popularity", ascending=False).filter(
	items=filter_columns).drop(["count", "popularity"], 1)
heatmap_data["loudness_01"] = (heatmap_data["loudness"] - min(heatmap_data["loudness"]))/(
		max(heatmap_data["loudness"])-min(heatmap_data["loudness"]))
heatmap_data["tempo_01"] = (heatmap_data["tempo"] - min(heatmap_data["tempo"]))/(
		max(heatmap_data["tempo"])-min(heatmap_data["tempo"]))
heatmap_head = heatmap_data.head(10)
