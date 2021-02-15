from data import *
import wikipedia


#for example: http://127.0.0.1:5000/info/Post-impressionism/1943/vincent+van+gogh
def retrieve_info(genre, year, artist):
    year = float(year)
    ranges = float(1)
    dictionary = {}
    # genre = "Post-impressionism"
    # year = float(1943)
    # artist = 'vincent van gogh'

    w = wikipedia.page(genre)
    dictionary['genre'] = w.title

    dictionary['summary'] = wikipedia.summary(genre, sentences=3)

    dictionary['related_terms'] = wikipedia.search(genre)

    other = model_data.loc[model_data['artist_full_name'] == artist]

    if len(other) <= 5:
        print(other['artwork_name'])
    else:
        print(other[:5]['artwork_name'])

    dictionary['other_pieces_by_artist'] = other

    # print('artworks in same time period:')
    # type(model_data['creation_year'][0])

    return dictionary

# other art pieces created in same year
# year_df = model_data.loc[model_data['creation_year'].astype('float') < year+ranges]
# year_df = year_df.loc[year_df['creation_year'].astype('float') > year-ranges]
