import os
import json
import re
import spacy
from sklearn.manifold import TSNE
import numpy as np
import pandas as pd

nlp = spacy.load('en')
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, './seekingalpha_nlp.json')

companies_vectors = {}
titles_vec = []
limit = 100
count = 0

with open(file_path, 'r') as companies:
	companies = json.load(companies)
	for symbol in companies:
		if count >= limit: break
		count = count + 1
		company = companies[symbol]
		for news in company:
			# take title of the news as a test
			title = news['title']
			for word in title:
				word_vec = nlp.vocab[word].vector
				titles_vec.append(word_vec)
				print word, word_vec

X = np.array(titles_vec)
model = TSNE()
twod_data = model.fit_transform(X)
twod_data = pd.DataFrame(twod_data, columns=[u'x_coord', u'y_coord'])
print twod_data

from bokeh.plotting import figure, show, output_notebook
from bokeh.models import HoverTool, ColumnDataSource, value

twod_data = ColumnDataSource(twod_data)
tsne_plot = figure(title=u'Stock news title word embedding', plot_width=800, plot_height=800, tools=(u'pan, wheel_zoom, box_zoom, box_select, resize, reset'))
tsne_plot.circle(u'x_coord', u'y_coord', source=twod_data, color=u'blue', line_alpha=0.2, fill_alpha=0.1, size=5, hover_line_color=u'black')
show(tsne_plot)