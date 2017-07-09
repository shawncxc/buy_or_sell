import os
import json
import re
import spacy
import string
from datetime import date, timedelta

def remove_tabs(token):
	return ''.join(token.split('\t'))

def remove_linebreaker(token):
	return ''.join(token.split('\n'))

def remove_linebreaker_tabs(token):
	return remove_linebreaker(remove_tabs(token))

def is_useless(token):
	useless_types = ['ADP', 'CONJ', 'CCONJ', 'NUM', 'DET', 'PUNCT', 'SYM'];
	return len(token) <= 2 or token.is_digit or token.is_punct or token.like_num or token.is_stop or token.pos_ in useless_types

# "Thu, Jun. 22, 12:04 PM" <-> "06/22/2017"
# "Nov. 30, 2016, 3:18 PM" <-> "11/30/2016"
def convert_date(date_str):
	month_table = {
		'Dec': '12',
		'Nov': '11',
		'Oct': '10',
		'Sep': '09',
		'Aug': '08',
		'Jul': '07',
		'Jun': '06',
		'May': '05',
		'Apr': '04',
		'Mar': '03',
		'Feb': '02',
		'Jan': '01'
	}

	date_str = re.sub(r'[^\w\s]', '', date_str)
	date_str = date_str.split();
	first_pos = date_str[0]
	if first_pos == 'Today':
		today = date.today()
		return str(today.month) + '/' + str(today.day) + '/' + str(today.year)
	if first_pos == 'Yesterday':
		yesterday = date.today() - timedelta(days=1)
		return str(yesterday.month) + '/' + str(yesterday.day) + '/' + str(yesterday.year)
	second_pos = date_str[1]
	thrid_pos = int(date_str[2])
	if thrid_pos >= 1000:
		year = str(thrid_pos)
		month = month_table[first_pos]
		day = second_pos
		if len(day) == 1: day = '0' + day
		return month + '/' + day + '/' + year
	else:
		year = str(date.today().year)
		month = month_table[second_pos]
		day = str(thrid_pos)
		if len(day) == 1: day = '0' + day
		return month + '/' + day + '/' + year

def find_delta(symbol, date_str):
	script_dir = os.path.dirname(__file__)
	file_path = os.path.join(script_dir, '../ticker/stock_history.json')
	with open(file_path, 'r') as stock_history:
		stock_history = json.load(stock_history)
		his = stock_history[symbol]
		for price in his:
			if price['date'] == date_str:
				return (price['close'] - price['open']) / price['open'] * 100

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
			converted_date = convert_date(single_news['date'])
			delta = find_delta(company, converted_date)
			single_news_nlp = {
				'title': [],
				'content': [],
				'date': converted_date,
				'delta': delta
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
			print company, single_news_nlp["date"], single_news_nlp["delta"]

file_path = os.path.join(script_dir, './seekingalpha_nlp.json')
with open(file_path, 'w+') as result_file:
	json.dump(companies_dict_nlp, result_file)