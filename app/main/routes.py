from flask import render_template, request, jsonify
import os, json

from decimal import Decimal

import pandas as pd
import numpy as np

from app import models, plots, data
from . import main


@main.route('/', methods=['GET'])
def index():
	return render_template("home.html")


@main.route('/bokeh', methods = ['GET', 'POST'])
def bokeh():
	property_type = request.args.get("property_type")
	rental_price = request.args.get("rental_price")
	surface_area = request.args.get("surface_area")

	if property_type is None:
		property_type = 'WCORHUUR_P'
		rental_price = 'WHUURTSLG_P'
		surface_area = 'WOPP0040_P'

	return render_template("bokeh.html",
		all_property_types=data.all_property_types, all_property_types_text=data.all_property_types_text,
		all_rental_prices=data.all_rental_prices, all_rental_prices_text=data.all_rental_prices_text,
		all_surface_areas=data.all_surface_areas, all_surface_areas_text=data.all_surface_areas_text,
		selected_property_type=property_type, selected_rental_price=rental_price, selected_surface_area=surface_area)


@main.route("/data", methods=['GET'])
def get_data():
	area = request.args.get("area")
	
	property_type = request.args.get("property")
	rental_price = request.args.get("price")
	surface_area = request.args.get("surface")
	plot = request.args.get("plot")

	query_input = []
	for idx, var in enumerate([surface_area, rental_price, property_type]):
		vars_query_input = [0] * len(data.all_var_types[idx])
		idx_query_var = data.all_var_types[idx].index(var)
		vars_query_input[idx_query_var] = 100
		query_input.extend(vars_query_input)

	#reshape query_input to correct format for input to our model
	query_input = np.array(query_input).reshape(1, -1)

	#retrain model based on new data
	trained_model = models.train_model(data.model_data, data.area_names, data.model_vars)

	#have our trained model make a prediction based on our query input
	_, probabilities = models.pred_proba(model=trained_model, input_vars=query_input)
	proba_idx = np.where(probabilities[0] == np.amax(probabilities[0]))
	proba_idx = proba_idx[0][0]
	
	#determine the index of the predicted area within the returned probabiblities array
	pred_area = data.area_names[proba_idx]
	proba = probabilities[0][proba_idx]
	proba = '%.3f' % Decimal(proba)

	#determine how the prediction probability of our previously predicted area has changed 
	#due to the change in data variables of this area
	if area is not None:
		proba_idx = data.area_names.index(area)
		new_proba_prev_area = probabilities[0][proba_idx]
		new_proba_prev_area = '%.3f' % Decimal(new_proba_prev_area)
		plot_area = area
	else:
		new_proba_prev_area = None
		plot_area = pred_area

	del probabilities
		
	if plot is not None:
		plot_data = data.model_data.loc[data.model_data['area_name'] == plot_area]
		plot_data = plot_data.loc[:, data.model_vars]
		plot = plots.create_hbar(plot_area, plot_data)
		return jsonify(prediction=pred_area, prediction_proba=proba, 
				area_changed_proba=new_proba_prev_area, plotData=plot)
	else:
		return jsonify(prediction=pred_area, prediction_proba=proba, 
				area_changed_proba=new_proba_prev_area)

	


@main.route('/d3', methods = ['GET', 'POST'])
def d3():
	area_name = request.args.get("area_name")

	if area_name is None:
		area_name = "Centrum-West"

	plot_data = data.stats_ams.loc[data.stats_ams['area_name'] == area_name]
	plot_data = plot_data.drop(['area_name', 'area_code'], axis=1)
	plot_data = plot_data.to_json(orient='records')

	meta_data = data.stats_ams_meta.to_json(orient='records')
	return render_template("d3.html", data=plot_data, meta_data=meta_data,
		x_variables=data.model_vars, area_names=data.area_names, selected_area_name=area_name)

