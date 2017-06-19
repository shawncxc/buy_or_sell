import os
import requests
import lxml.html
import json
import re

# Date  Open    High    Low Close / Last    Volum

def get_all_history():
    hisdict = {}
    duration = '5d'
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, '../ticker/companies.json')
    with open(file_path, 'r') as file:
        tickers = json.load(file)
        for ticker in tickers:
            symbol = ticker['symbol']
            try:
                records = get_stock_history(duration, symbol)
                hisdict[symbol] = records
            except:
                print 'Error when get_stock_history for:', symbol
                continue

    stock_history = os.path.join(script_dir, '../result/stock_history.json')
    with open(stock_history, 'w+') as file:
        json.dump(hisdict, file)

    print "complete"
    return hisdict

def get_stock_history(duration, symbol):
    session = requests.Session()
    session.headers = {
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type': 'application/json',
    }
    url = 'http://www.nasdaq.com/symbol/' + symbol.lower() + '/historical'
    payload = '{duration}|false|{symbol}'.format(duration = duration, symbol = symbol.upper())
    req = session.post(url, data = payload)
    try:
        return process_text(req.text)
    except:
        print 'Error when process text for:', symbol
        return []
    
def process_text(text):
    records = []
    text = ''.join(text.split())
    text = re.findall(r'<tr><td>.+<\/tr>', text)[0]
    text = re.findall(r'<tr>(.*?)<\/tr>', text)
    for record in text:
        record = re.findall(r'<td>(.*?)<\/td>', record)
        record_obj = {
            'date': record[0],
            'open': float(record[1]),
            'high': float(record[2]),
            'low': float(record[3]),
            'close': float(record[4]),
            'volum': float(record[5].replace(',', ''))
        }
        records.append(record_obj)
    print record_obj
    return records

get_all_history()
