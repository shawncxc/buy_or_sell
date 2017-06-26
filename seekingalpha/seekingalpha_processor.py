import os
import json
import re
import spacy

def remove_tabs(token):
	return ''.join(token.split('\t'))

def remove_linebreaker(token):
	return ''.join(token.split('\n'))

def remove_linebreaker_tabs(token):
	return remove_linebreaker(remove_tabs(token))

def is_useless(token):
	useless_types = ['ADP', 'CONJ', 'CCONJ', 'NUM', 'DET', 'PUNCT', 'SYM'];
	return len(token) <= 2 or token.is_digit or token.is_punct or token.like_num or token.pos_ in useless_types

nlp = spacy.load('en')
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, './seekingalpha.json')

companies_dict_nlp = {}

with open(file_path, 'r') as companies:
	companies = json.load(companies)
	for company in companies:
		news = companies[company]
		companies_dict_nlp[company] = []
		for i in range(0, len(news)):
			single_news = news[i]
			single_news_nlp = {
				'title': [],
				'content': [],
				'date': single_news['date']
			}
			
			title_nlp = nlp(single_news['title'])
			for token in title_nlp:
				lemma = remove_linebreaker_tabs(token.lemma_)
				if is_useless(token): continue
				single_news_nlp['title'].append(lemma)

			content_nlp = nlp(single_news['content'])
			for token in content_nlp:
				lemma = remove_linebreaker_tabs(token.lemma_)
				if is_useless(token): continue
				single_news_nlp['content'].append(lemma)

			companies_dict_nlp[company].append(single_news_nlp)
			print single_news_nlp

file_path = os.path.join(script_dir, './seekingalpha_nlp.json')
with open(file_path, 'w+') as result_file:
	json.dump(companies_dict_nlp, result_file)