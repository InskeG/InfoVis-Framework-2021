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


model_vars = all_artwork_name





def update_data(g_type, var, new_value):
    model_data.loc[model_data['artwork_name']==g_type, var] = new_value

    return model_data