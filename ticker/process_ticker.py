import os
import csv
import json

def dump_tickers_into_json():
	companies = []
	script_dir = os.path.dirname(__file__)
	csv_file = os.path.join(script_dir, './companylist.csv')
	with open(csv_file) as tickers:
		tickers = csv.DictReader(tickers)
		for ticker in tickers:
			market_cap = float(ticker['MarketCap'])
			two_billion = 2000000000
			if market_cap >= two_billion:
				companies.append({ 'name': ticker['Name'] })

		companylist_json_file = os.path.join(script_dir, './companies.json')
		with open(companylist_json_file, 'w+') as file:
			json.dump(companies, file)
