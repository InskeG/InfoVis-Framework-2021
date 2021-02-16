from data import *
import pandas as pd  
import wikipedia


#for example: http://127.0.0.1:5000/info/impressionism/1954/vincent%20van%20gogh
# year is nodig om genre te bepalen naderhand want die staan niet in dataset
def retrieve_info(genre, year, artist):
    dictionary = {}

    w = wikipedia.page(genre)
    dictionary['genre'] = w.title

    dictionary['summary'] = wikipedia.summary(genre, sentences=3)

    dictionary['related_terms'] = wikipedia.search(genre)

    other = model_data.loc[model_data['artist_full_name'] == artist]

    if len(other) <= 5:
        dictionary['other_pieces_by_artist'] = pd.Series.tolist(other['artwork_name'])
    else:
        dictionary['other_pieces_by_artist'] = pd.Series.tolist(other[:5]['artwork_name'])

    return dictionary


# print('artworks in same time period:')
# other art pieces created in same year
    year_df = model_data.loc[model_data['creation_year'].astype('float') < year+ranges]
    year_df = year_df.loc[year_df['creation_year'].astype('float') > year-ranges]

    dictionary['same_year'] = pd.Series.tolist(year_df)