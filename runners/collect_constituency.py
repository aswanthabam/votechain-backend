import requests
from bs4 import BeautifulSoup
import json

link = "https://en.wikipedia.org/wiki/List_of_constituencies_of_the_Lok_Sabha"
domain = 'https://en.wikipedia.org'
data = {}
page = requests.get(link)
soup = BeautifulSoup(page.text, 'html.parser')
spans = soup.find_all('span','mw-headline')
tables = soup.find_all('table','wikitable')

def name_formatter(name):
    name = name.replace('\n',' ')
    return name.split('(')[0].lower().replace(' ',''), ' '.join([x for x in name.split('(')[0].title().split(' ') if x != ''])
i = 0
un_st = False
for span in spans:
    _id,name = name_formatter(span.text)
    if  _id == 'delimitationofconstituencies' or _id == 'summary':continue
    if _id == 'seealso':break
    if _id == 'unionterritories':
        un_st = True
        continue
    i+=1
    print(name)
    data[_id] = {
        'name': name,
        'districts': {}
    }
    table = tables[i]
    trs = table.find('tbody').find_all('tr')[1:]
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) == 0:continue
        _dis_id,name = name_formatter(tds[1].text)
        print(' --',name)
        _link = domain + tds[1].find('a')['href']
        data[_id]['districts'][_dis_id] = {
            'name': name,
            'id': _dis_id,
            'link': _link,
            'constituency':{}
        }
        if un_st:continue
        res = requests.get(_link)
        soup2 = BeautifulSoup(res.text, 'html.parser')
        table2 = soup2.find('table','wikitable')
        if(table2 == None):continue
        trs2 = table2.find('tbody').find_all('tr')[1:]
        for tr2 in trs2:
            tds2 = tr2.find_all('td')
            if len(tds2) == 0:continue
            if len(tds2) == 1:
                _con_id,name = name_formatter(tds2[0].text)
            else : _con_id,name = name_formatter(tds2[1].text)
            print('    --',name)
            try:
                if len(tds2) == 1:_link = domain + tds2[0].find('a')['href']
                else :_link = domain + tds2[1].find('a')['href']
            except:_link = None
            data[_id]['districts'][_dis_id]['constituency'][_con_id] = {
                'name': name,
                'id': _con_id,
                'link': _link,
            }

_data = json.dumps(data, indent=2)
with open('constituency.json', 'w') as f:
    f.write(_data)
# print(data['kerala']['districts']['kannur'])
