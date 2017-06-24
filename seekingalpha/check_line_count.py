import os
import json

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '../ticker/companies.json')
with open(file_path, 'r') as file:
	file = json.load(file)
	print len(file)

file_path = os.path.join(script_dir, './seekingalpha.json')
with open(file_path, 'r') as file:
	file = json.load(file)
	print len(file)