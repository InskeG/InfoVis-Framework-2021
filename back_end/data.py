import math
import numpy as np
import pandas as pd
import pickle
import os
import re

from collections import Counter


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

DATA_PATH = 'data/paintings_data.pk'
TIMELINE_PATH = 'data/timeline_data.pk'
FEATURED_ARTISTS = ['bosch', 'vinci', 'greco', 'caravaggio', 'rubens', 'vermeer',
                    'dyck', 'hals', 'steen', 'turner', 'ingres', 'blake', 'delacroix',
                    'gogh', 'degas', 'monet', 'watteau', 'lemoyne']

paintings = pd.DataFrame()
all_artists = []
all_artist_last_names = []

if not os.path.exists(DATA_PATH):
    SCHOOL_MAP = {
        'Italia': 'italian',
        'unknown': 'other',
        'Catalan, Ferrocarril, Perimetro Urbano Pereira, Pereira, Risaralda, Colombia': 'other',
        'flemish': 'belgian',
        'España': 'spanish',
        'France métropolitaine, France': 'french',
        'south': 'other',
        'netherlandish': 'dutch',
        'north': 'other',
        'bavaria,': 'other',
        'Deutschland, Europe': 'german',
        'franco-flemish': 'belgian',
        'Nederland': 'dutch',
        'Österreich': 'austrian',
        'Great Britain, Richmondshire, North Yorkshire, Yorkshire and the Humber, England, UK': 'british',
        'Portugese Fort, كمران, الحديدة, اليمن': 'portuguese',
        'Schweiz/Suisse/Svizzera/Svizra': 'swiss',
        'Bohemian, Plaquemines Parish, Louisiana, 70083, United States of America': 'bohemian',
        'Russian, Municipio Benítez, Sucre, Venezuela': 'russian',
        'Irish, Nahant, Lawrence County, South Dakota, 57778, United States of America': 'irish',
        'Danmark': 'danish',
        'United States of America': 'american',
        'Other, Corozal, Corozal District, Corozal, 0000, Belize': 'other',
        'Scotland, UK': 'scottish',
        'België / Belgique / Belgien': 'belgian',
        'norwegian,': 'norwegian',
        'Sverige': 'swedish',
        np.nan: 'other'
    }

    # csv = pd.read_csv('data/omniart_v3_datadump.csv')
    paintings = model_data[
        (model_data['artwork_type'].isin(['painting', 'drawing']))
        & (~model_data['artist_full_name'].str.contains(
            r'unknown|unidentified', na=False,
        ))
        & (model_data['artwork_name'] != 'unknown')].copy()
    paintings['creation_year'] = pd.to_numeric(paintings['creation_year'])
    paintings.sort_values('creation_year', inplace=True)
    paintings = paintings[paintings['creation_year'] > 0][[
        'artwork_name',
        'artist_full_name',
        'artist_last_name',
        'creation_year',
        'school',
        'image_url',
    ]]
    paintings['school'] = paintings['school'].replace(SCHOOL_MAP).str.lower()

    valid_artists = paintings[
        paintings['artist_full_name'].str.match(r"^((?!painter|master|\d)(((?![\d])\w){2,}|\s))+$", flags=re.UNICODE,
                                                na=False)].groupby('artist_full_name').size()
    all_artists = list(np.unique(valid_artists[valid_artists > 20].index.tolist()))

    all_artist_last_names = list(pd.unique(paintings['artist_last_name']))

    with open(DATA_PATH, 'wb') as file:
        pickle.dump((paintings, all_artists, all_artist_last_names), file)
else:
    with open(DATA_PATH, 'rb') as file:
        paintings, all_artists, all_artist_last_names = pickle.load(file)


def get_artists():
    # stats_art = pd.read_csv('./data/omniart_v3_datadump.csv')
    # model_data = stats_art.copy()
    # model_data = model_data.drop(model_data[model_data['artist_full_name'] == 'unknown'].index)
    # model_data = model_data.drop(model_data[model_data['creation_year'] == 'unknown'].index)
    all_artist_text = sorted(model_data['artist_full_name'].astype(str).unique().tolist())[:100]
    # all_artist_text = [x.strip(' ') for x in all_artist_text]
    art_list = []
    for x in all_artist_text:
        art_list.append({'artist': x.strip(' ')})

    return art_list



def get_line_graph(artist):
    # stats_art = pd.read_csv('./data/omniart_v3_datadump.csv')
    # model_data = stats_art.copy()
    # model_data = model_data.drop(model_data[model_data['artist_full_name'] == 'unknown'].index)
    # model_data = model_data.drop(model_data[model_data['creation_year'] == 'unknown'].index)

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


def get_model_data():
    all_artist = sorted(paintings['artist_full_name'].astype(str).unique().tolist())[:100]
    all_artist = [x.strip(' ') for x in all_artist]

    all_artist_text = sorted(paintings['artist_full_name'].astype(str).unique().tolist())[:100]
    all_artist_text = [x.strip(' ') for x in all_artist_text]

    all_artwork_name = sorted(paintings['artwork_name'].astype(str).unique().tolist())[:100]
    all_artwork_name_text = sorted(paintings['artwork_name'].astype(str).unique().tolist())[:100]

    all_years = (paintings['creation_year'].unique().tolist())

    l = [round(float(x)) for x in all_years if type(x) == str and x != 'nan']
    l.sort()
    creation_year = np.arange(min(l), max(l), 500).tolist()

    return all_artwork_name


def get_timeline_data(artists=None, adding=False):
    if artists is None:
        artists = FEATURED_ARTISTS

    if adding:
        for i, artist in enumerate(artists):
            if artist not in all_artist_last_names:
                artist_last_name = paintings[paintings['artist_full_name'] == artist]
                if not artist_last_name.empty:
                    artists[i] = artist_last_name.iloc[0]['artist_last_name']

    if not os.path.exists(TIMELINE_PATH) or artists != FEATURED_ARTISTS:
        featured_paintings = paintings[paintings['artist_last_name'].isin(artists)]
        year_dict = Counter(featured_paintings['creation_year'].to_numpy(dtype=int))

        j = 0
        MAX_LANES = 20
        timeline_data = [{'group': str(0), 'data': [{'label': '', 'data': []}]}]
        for i, painting in featured_paintings.iterrows():
            while True:
                if j >= len(timeline_data):
                    timeline_data.append({'group': str(j), 'data': [{'label': '', 'data': []}]})

                max_paintings_per_year = math.ceil(year_dict[int(painting['creation_year'])] / MAX_LANES)
                possible_months = np.unique(np.linspace(0, 12, max_paintings_per_year + 1) % 12)

                month_start = None
                dates_in_lane = [x['timeRange'][0] for x in timeline_data[j]['data'][0]['data']]
                for month in possible_months:
                    if {'year': painting['creation_year'], 'month': month} not in dates_in_lane:
                        month_start = month
                        break

                if month_start is None:
                    j += 1
                else:
                    t_start = {'year': painting['creation_year'], 'month': month_start}

                    end_month = possible_months[(np.where(possible_months == month_start)[0] + 1) %
                                                len(possible_months)][0]
                    t_end = {'year': painting['creation_year'] + (1 if end_month == 0 else 0), 'month': end_month}

                    timeline_data[j]['data'][0]['data'].append({
                        'timeRange': [t_start, t_end],
                        'val': f"{painting['artist_last_name']}",
                        'labelVal': f"{painting['artwork_name']}<br/>({painting['artist_full_name']})"
                    })
                    j = 0
                    break

        if artists == FEATURED_ARTISTS:
            with open(TIMELINE_PATH, 'wb') as file:
                pickle.dump(timeline_data, file)
    else:
        with open(TIMELINE_PATH, 'rb') as file:
            timeline_data = pickle.load(file)

    return timeline_data, artists


def update_data(g_type, var, new_value):
    paintings.loc[paintings['artwork_name'] == g_type, var] = new_value
    return paintings
