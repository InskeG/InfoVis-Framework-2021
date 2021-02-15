from data import *
import wikipedia




genre = "Post-impressionism"
year = float(1943)
ranges = float(1)
artist = 'vincent van gogh'



w = wikipedia.page(genre)
print(w.title)

print(wikipedia.summary(genre, sentences=3))

print('-----------')
print("Related terms:")
print(wikipedia.search(genre))


model_data

print('artworks in same time period:')
type(model_data['creation_year'][0])


print('Other art pieces by this artist')
year_df = model_data.loc[model_data['artist_full_name'] == artist]

if len(year_df) <= 5:
    print(year_df['artwork_name'])
else:
    print(year_df[:5]['artwork_name'])


# other art pieces created in same year
# year_df = model_data.loc[model_data['creation_year'].astype('float') < year+ranges]
# year_df = year_df.loc[year_df['creation_year'].astype('float') > year-ranges]
