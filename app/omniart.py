import math
import re

import numpy as np
import os
import pandas as pd
import pickle
from collections import Counter

path = 'app/timeline_data.pk'
if not os.path.exists(path):
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

    csv = pd.read_csv('app/omniart_v3_datadump.csv')
    paintings = csv[(csv['artwork_type'].isin(['painting', 'drawing'])) &
                    (~csv['artist_full_name'].str.contains(r'unknown|unidentified', na=False)) &
                    (csv['artwork_name'] != 'unknown')].copy()
    paintings['creation_year'] = pd.to_numeric(paintings['creation_year'])
    paintings.sort_values('creation_year', inplace=True)
    paintings = paintings[paintings['creation_year'] > 0][['artwork_name', 'artist_full_name', 'artist_last_name',
                                                           'creation_year', 'school', 'image_url']]
    paintings['school'] = paintings['school'].replace(SCHOOL_MAP).str.lower()
    # paintings = paintings.sample(5000)

    featured_artists = ['michelangelo', 'bosch', 'vinci', 'greco', 'caravaggio', 'rubens', 'vermeer',
                        'rembrandt', 'dyck', 'hals', 'beale', 'steen', 'turner', 'ingres', 'blake', 'delacroix',
                        'gogh', 'degas', 'monet', 'magritte', 'kandinsky', 'picasso', 'renoir', 'warhol', 'banksy',
                        'füger', 'watteau', 'bencovich', 'hogarth', 'lemoyne', 'rococo', 'panini']

    paintings = paintings[paintings['artist_last_name'].isin(featured_artists)]
    year_dict = Counter(paintings['creation_year'].to_numpy(dtype=int))

    foo = paintings[paintings['artist_full_name'].str.match(r"^((?!painter|master|\d)(((?![\d])\w){2,}|\s))+$", flags=re.UNICODE, na=False)].groupby('artist_full_name').size()
    bar = foo[foo > 20]

    j = 0
    MAX_LANES = 20
    timeline_data = [{'group': str(0), 'data': [{'label': '', 'data': []}]}]
    for i, painting in paintings.iterrows():
        while True:
            if j >= len(timeline_data):
                timeline_data.append({'group': str(j), 'data': [{'label': '', 'data': []}]})

            max_paintings_per_year = math.ceil(year_dict[int(painting['creation_year'])] / MAX_LANES)
            possible_months = np.unique(np.linspace(0, 12, max_paintings_per_year + 1, dtype=int) % 12)

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

                end_month = possible_months[(np.where(possible_months == month_start)[0] + 1) % len(possible_months)][0]
                t_end = {'year': painting['creation_year'] + (1 if end_month == 0 else 0), 'month': end_month}

                timeline_data[j]['data'][0]['data'].append({
                    'timeRange': [t_start, t_end],
                    'val': f"{painting['artist_last_name']}",
                    'labelVal': f"{painting['artwork_name']}<br/>({painting['artist_full_name']})"
                })
                j = 0
                break

    with open(path, 'wb') as file:
        pickle.dump(timeline_data, file)
else:
    with open(path, 'rb') as file:
        timeline_data = pickle.load(file)
