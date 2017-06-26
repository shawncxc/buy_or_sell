# https://seekingalpha.com/symbol/AAPL/news
# https://seekingalpha.com/symbol/AAPL/news/more_news_all?page=3

import os
import json
import re
import urllib2

seeking_dict = {}
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '../ticker/companies.json')
with open(file_path, 'r') as companies:
	companies = json.load(companies)
	for company in companies:
		symbol = company['symbol']
		seeking_dict[symbol] = []
		for page in range(1, 2):
			url = 'https://seekingalpha.com/symbol/{symbol}/news/more_news_all?page={page}'.format(symbol=symbol, page=page)
			req = urllib2.Request(url)
			req.add_header('User-agent', 'Mozilla/5.0')
			try:
				response = urllib2.urlopen(req)
				the_page = response.read()
				the_page = json.loads(the_page)
				if the_page['html'] == '': break
			except:
				continue
			the_page = the_page['html']
			titles = re.findall('target=_self>(.*.)</a></div>', the_page)
			contents = re.findall('<ul><li>(.*.)</li></ul>', the_page)
			dates = re.findall('<span class="date pad_on_summaries">(.*.)</span>', the_page)
			for i in range(0, min(len(titles), len(contents), len(dates))):
				single_news = {
					'title': titles[i],
					'content': re.sub('<[^<]+?>', ' ', contents[i]),
					'date': dates[i]
				}
				seeking_dict[symbol].append(single_news)
			print url

file_path = os.path.join(script_dir, './seekingalpha.json')
with open(file_path, 'w+') as file:
    json.dump(seeking_dict, file)



