import os
import json

def seekingalpha_processor():
	news_dict = {}

	script_dir = os.path.dirname(__file__)
	file_path = os.path.join(script_dir, './seekingalpha.json')
	with open(file_path) as data_file:
		data = json.load(data_file)
		for news in data:
			symbol = news['symbol']
			title = news['title']
			if symbol in news_dict:
				news_dict[symbol].append(title)
			else:
				news_dict[symbol] = [title];

	for symbol in news_dict:
		if len(news_dict[symbol]) > 1:
			print symbol, news_dict[symbol]
