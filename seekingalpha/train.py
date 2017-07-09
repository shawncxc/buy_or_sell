import os
import json
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, './training_data.json')
with open(file_path, 'r') as training_data:
	training_data = json.load(training_data)
	X = training_data['X']
	Y = training_data['Y']
	# clf = RandomForestClassifier(n_estimators=10)
	# clf = clf.fit(X, Y)
	reg = linear_model.LinearRegression()
	reg.fit(X, Y)
	pickle.dump(reg, open('linear_model.sav', 'wb'))
	print 'model saved'
