import os
import json
import spacy

def avg_vec(vecs):
	avg_vec = []
	dimension = len(vecs[0])
	total_vec = len(vecs)
	for i in range(0, dimension):
		avg_vec.append(0)
	for vec in vecs:
		for i in range(0, dimension):
			avg_vec[i] = avg_vec[i] + vec[i]
	for i in range(0, dimension):
		avg_vec[i] = avg_vec[i] / total_vec
	return avg_vec

def get_training_data():
	nlp = spacy.load('en')
	training_data = {}
	X = []
	Y = []
	script_dir = os.path.dirname(__file__)
	file_path = os.path.join(script_dir, './seekingalpha_nlp.json')
	with open(file_path, 'r') as companies:
		companies = json.load(companies)
		for symbol in companies:
			company = companies[symbol]
			print symbol, len(company)
			total_news = str(len(company))
			current_news = 0
			for news in company:
				current_news = current_news + 1
				delta = news['delta']
				if delta is None: continue
				word_vecs = []
				title = news['title']
				for word in title:
					word_vec = nlp.vocab[word].vector
					word_vecs.append(word_vec)
				content = news['content']
				for word in content:
					word_vec = nlp.vocab[word].vector
					word_vecs.append(word_vec)
				X.append(avg_vec(word_vecs))
				Y.append(delta)
				print symbol + str(current_news) + '/' + total_news
		training_data['X'] = X
		training_data['Y'] = Y

	file_path = os.path.join(script_dir, './training_data.json')
	with open(file_path, 'w+') as file:
	    json.dump(training_data, file)