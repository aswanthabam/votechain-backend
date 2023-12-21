import json, requests
from bs4 import BeautifulSoup

f =  open('constituency.json', 'r') 
data = json.load(f)

for _id,_val in data.items():
    for _dis_id,_dis_val in _val['districts'].items():
        data[_id]['districts'][_dis_id]['description'] = None
        data[_id]['districts'][_dis_id]['image'] = None
        try:
            _link = _dis_val['link']
            print(_dis_val['name'])
            res = requests.get(_link)
            soup = BeautifulSoup(res.text, 'html.parser')
            description = soup.find('div','mw-content-ltr').find_all('p')[1]
            data[_id]['districts'][_dis_id]['description'] = description.text
            data[_id]['districts'][_dis_id]['image'] = soup.find('table','infobox vcard').find('img')['src']
            for _con_id,_con_val in _dis_val['constituency'].items():
                data[_id]['districts'][_dis_id]['constituency'][_con_id]['description'] = None
                data[_id]['districts'][_dis_id]['constituency'][_con_id]['image'] = None
                try:
                    _link = _con_val['link']
                    print('    ',_con_val['name'])
                    res = requests.get(_link)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    description = soup.find('div','mw-content-ltr').find_all('p')[1]
                    data[_id]['districts'][_dis_id]['constituency'][_con_id]['description'] = description.text
                    data[_id]['districts'][_dis_id]['constituency'][_con_id]['image'] = soup.find('table','infobox vcard').find('img')['src']
                except Exception as err:
                    print(err)
                    continue
        except Exception as err:
            print(err)
            continue

with open('constituency.json', 'w') as f:
    f.write(json.dumps(data, indent=2)) 