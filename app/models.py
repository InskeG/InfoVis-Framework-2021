import os
from sklearn.svm import SVC

def linearSVC(X, y):
	model = SVC(kernel='linear', probability=True)
	model.fit(X, y)

	return model

def train_model(df_data, target, var_cols):
	model_data = df_data.loc[:, var_cols]
	model_data = model_data.to_numpy()
	trained_model = linearSVC(model_data, target)

	return trained_model

def pred_proba(model, input_vars):
	label = model.predict(input_vars)
	label = label[0]
	prob = model.predict_proba(input_vars)

	return label, prob
