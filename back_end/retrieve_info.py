from data import *
import pandas as pd  
import wikipedia


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


