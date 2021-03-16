import itertools
import numpy as np
import pandas as pd
import wikipedia

from colour import Color

from .data import *


#for example: http://127.0.0.1:5000/info/impressionism/1943/
# year is nodig om genre te bepalen naderhand want die staan niet in dataset
def retrieve_info(genre, year):
    year = float(year)
    ranges = float(1)
    dictionary = {}

    w = wikipedia.page(genre)
    dictionary['genre'] = w.title

    dictionary['summary'] = wikipedia.summary(genre, sentences=3)


    # print('artworks in same time period:')
    # other art pieces created in same year
    year_df = model_data.loc[model_data['creation_year'].astype('float') < year+ranges]
    year_df = year_df.loc[year_df['creation_year'].astype('float') > year-ranges]

    # print(year_df)
    year_list = pd.Series.tolist(year_df['artwork_name'])
    if len(year_list) < 5:
        dictionary['same_year/genre'] = pd.Series.tolist(year_df['artwork_name'])
    else:
        dictionary['same_year/genre'] = pd.Series.tolist(year_df['artwork_name'])[:5]

    dictionary['related_terms'] = wikipedia.search(genre)

    # other = paintings.loc[paintings['artist_full_name'] == artist]

    return dictionary


def _get_artist_histograms(artists=None):
    if not artists:
        artists = FEATURED_ARTISTS

    result = {}

    for artist in artists:
        # Gather all works by this artist.
        works = model_data[model_data.artist_last_name == artist]
        # colors = works.color_pallete.dropna()
        colors = works.dominant_color.dropna()

        # The data are a series of strings. These strings represent a list of
        # hex codes. We use `eval` to convert these strings to lists.
        # colors = itertools.chain.from_iterable(
        #     eval(f"[{','.join(colors.values)}]")
        # )
        hues = [Color(col).hue for col in colors]

        if len(hues) == 0:
            continue

        hist, edges = np.histogram(hues, bins=11, range=(0, 1), density=True)

        print(hues, hist)

        x_values = [
            0.5 * (first + second)
            for first, second in zip(edges[:-1], edges[1:])
        ]

        result[artist] = list(zip(x_values, hist))

    return result
