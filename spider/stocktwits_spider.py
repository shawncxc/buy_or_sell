import os
import requests
import lxml.html
import json
import re
 
session = requests.Session()
 
req = session.get("https://stocktwits.com/symbol/AAPL")
e = lxml.html.fromstring(req.text)
csrf_token = e.xpath('//meta[@name="csrf-token"]/@content')[0]
scripts = e.xpath('//script')
for script in scripts:
    if 'max_id' in str(script.text):
        max_id  = int(re.findall('max_id: (\d+),', script.text)[0])
        item_id = int(re.findall('poll_id: \'(.*)\', symbol:', script.text)[0])
        print item_id
 
session.headers = {
    'X-CSRF-Token': csrf_token,
    'X-Requested-With':'XMLHttpRequest'
}
req = session.get("http://stocktwits.com/streams/poll?stream=symbol&max={}&stream_id={}&substream=top&item_id={}".format(max_id, item_id, item_id))
json_data = json.loads(req.text)
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '../result/stocktwits.json')
with open(file_path, 'w+') as file:
    for message in json_data['messages']:
        if message['sentiment'] is not None:
            print message['sentiment']['class']
            print message['body']
    # json.dump(json_data['messages'], file)
# max_id = json_data['max']
# r = s.get("http://stocktwits.com/streams/poll?stream=symbol&max={}&stream_id={}&substream=top&item_id={}".format(max_id, item_id, item_id))