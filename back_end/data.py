import pandas as pd
import math
import re
import numpy as np


# Load data as panda dfs #

stats_art = pd.read_csv('./data/omniart_v3_datadump.csv')
##########################

model_data = stats_art.copy()
model_data = model_data.drop(model_data[model_data['artist_full_name'] == 'unknown'].index)
model_data = model_data.drop(model_data[model_data['creation_year'] == 'unknown'].index)



# print(model_data['school'].unique().tolist()[2])
# print(len(model_data[model_data['school'] == 'impressionism'].index))

#fixed lists of all vars + textual explanation of each var (for query menu)
all_artist = sorted(model_data['artist_full_name'].astype(str).unique().tolist())[:100]
all_artist = [x.strip(' ') for x in all_artist]

all_artist_text = sorted(model_data['artist_full_name'].astype(str).unique().tolist())[:100]
all_artist_text = [x.strip(' ') for x in all_artist_text]


all_artwork_name = sorted(model_data['artwork_name'].astype(str).unique().tolist())[:100]
all_artwork_name_text = sorted(model_data['artwork_name'].astype(str).unique().tolist())[:100]


all_years = (model_data['creation_year'].unique().tolist())
# all_years.remove('unknown')

l = []
for x in all_years:
    if type(x) == str and x !='nan':
        l.append(x)

l = [round(float(num)) for num in l]
l.sort()
creation_year = np.arange(min(l), max(l), 500).tolist()


def get_artists():
    stats_art = pd.read_csv('./data/omniart_v3_datadump.csv')
    model_data = stats_art.copy()
    model_data = model_data.drop(model_data[model_data['artist_full_name'] == 'unknown'].index)
    model_data = model_data.drop(model_data[model_data['creation_year'] == 'unknown'].index)
    all_artist_text = sorted(model_data['artist_full_name'].astype(str).unique().tolist())[:100]
    # all_artist_text = [x.strip(' ') for x in all_artist_text]
    art_list = []
    for x in all_artist_text:
        art_list.append({'artist': x.strip(' ')})

    return art_list



def get_line_graph(artist):
    stats_art = pd.read_csv('./data/omniart_v3_datadump.csv')
    model_data = stats_art.copy()
    model_data = model_data.drop(model_data[model_data['artist_full_name'] == 'unknown'].index)
    model_data = model_data.drop(model_data[model_data['creation_year'] == 'unknown'].index)

    line_graph = {}

    a = model_data['creation_year'].tolist()
    b = model_data['dominant_color'].tolist()
    c = model_data['artist_full_name'].tolist()


    for i, artist in enumerate(c):
        if artist not in line_graph.keys():
            line_graph[artist] = []
        line_graph[artist].append([a[i], b[i]])

    serie = []
    for datas in line_graph.values():
        serie.append( {
            'values': datas
        }
        )
    return line_graph, serie


# line_graph = {}

# a = model_data['creation_year'].tolist()
# b = model_data['dominant_color'].tolist()
# c = model_data['artist_full_name'].tolist()


# for i, artist in enumerate(c):
#     if artist not in line_graph.keys():
#         line_graph[artist] = []
#     line_graph[artist].append([a[i], b[i]])

# serie = []
# for datas in line_graph.values():
#     serie.append( {
#         'values': datas
#     }
#     )


# line_graph = list(zip(a, b))
# line_graph = list(map(list, line_graph)) 


# line_graph = []
# for index, row in model_data.iterrows():
#     line_graph.append([row['creation_year'], row['dominant_color'], row['artist_full_name']])


# line_graph = [[x['creation_year'], x['dominant_color'], x['artist_full_name']] for x in model_data]
















def update_data(g_type, var, new_value):
    model_data.loc[model_data['artwork_name']==g_type, var] = new_value

    return model_data