import pandas as pd
from . import models

# Load data as panda dfs #
stats_ams = pd.read_csv('app/data/ams_stats_infovis.csv')
stats_ams_meta = pd.read_csv("app/data/ams_stats_infovis_metadata.csv", sep=";")
##########################

model_data = stats_ams.copy()
model_vars = stats_ams.drop(['area_name', 'area_code', 'WOPPONB_P'], axis=1)
model_vars = model_vars.columns.tolist()
model_vars_text = ['Living space of 0-40 m2', 'Living space of 40-60 m2', 'Living space of 60-80 m2', 
'Living space of 80-100 m2', 'Living space of > 100 m2', 'Low rent (< 711 euro)', 'Middle high rent (711 - 971 euro)', 
'High rent (> 971 euro)', 'Housing corporation rental', 'Private rental']

area_names = stats_ams['area_name'].unique().tolist()

label_def = stats_ams_meta['Definition'].tolist()
label_extra = stats_ams_meta['Label_1'].tolist()
label_var = stats_ams_meta['Variabele'].tolist()

#fixed lists of all vars + textual explanation of each var (for query menu)
all_property_types = ['WCORHUUR_P', 'WPARTHUUR_P']
all_rental_prices = ['WHUURTSLG_P', 'WHUURMIDDEN_P', 'WHUURHOOG_P']
all_surface_areas = ['WOPP0040_P', 'WOPP4060_P', 'WOPP6080_P', 'WOPP80100_P', 'WOPP100PLUS_P']
all_property_types_text = ['Housing corporation rental', 'Private rental']
all_rental_prices_text = ['Low rent (< 711 euro)', 'Middle high rent (711 - 971 euro)', 'High rent (> 971 euro)']
all_surface_areas_text = ['Living space of 0-40 m2', 'Living space of 40-60 m2', 'Living space of 60-80 m2', 
'Living space of 80-100 m2', 'Living space of > 100 m2']
all_var_types = [all_surface_areas, all_rental_prices, all_property_types]

label_def_ordered = []
label_extra_ordered = []
for var in model_vars:
	idx = label_var.index(var)
	label_def_ordered.append(label_def[idx])
	label_extra_ordered.append(label_extra[idx])


def update_data(area, var, new_value):
    model_data.loc[model_data['area_name']==area, var] = new_value

    return model_data