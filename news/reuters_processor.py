import os
import json
import spacy

def remove_tabs(token):
	return ''.join(token.split('\t'))

def remove_linebreaker(token):
	return ''.join(token.split('\n'))

def remove_linebreaker_tabs(token):
	return remove_linebreaker(remove_tabs(token))

reuters_nlp = []
nlp = spacy.load('en')
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, './reuters.json')

with open(file_path, 'r') as news:
	news = json.load(news)
	for single_news in news:
		single_news_nlp = {}
		
		date = single_news['date']
		title = single_news['title']
		title_nlp = nlp(title)
		content = single_news['content']
		content_nlp = nlp(content)

		single_news_nlp['date'] = date
		single_news_nlp['title'] = []
		single_news_nlp['content'] = []
		for token in title_nlp:
			token = remove_linebreaker_tabs(token.lemma_)
			if len(token) <= 2: continue
			single_news_nlp['title'].append(token)

		for token in content_nlp:
			token = remove_linebreaker_tabs(token.lemma_)
			if len(token) <= 2: continue
			single_news_nlp['content'].append(token)

		reuters_nlp.append(single_news_nlp)

file_path = os.path.join(script_dir, './reuters_token.json')
with open(file_path, 'w+') as result_file:
        json.dump(reuters_nlp, result_file)