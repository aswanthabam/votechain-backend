import requests
import json

host = 'http://localhost:8000'

f = open('constituency.json', 'r')
data = json.load(f)

for _id,_val in data.items():
    _data = {
        'name': _val['name'],
    }
    res = requests.post(host+'/api/location/states/', data=_data)
    print(res.text)
    _val['id'] = json.loads(res.text)['data']['id']
    for _dis_id,_dis_val in _val['districts'].items():
        _data = {
            'state_id': _val['id'],
            'name': _dis_val['name'],
            'link': _dis_val['link'], 
            'description': _dis_val['description'],
            'image': _dis_val['image'],
            'state': _val['id'],
        }
        res = requests.post(host+'/api/location/districts/', data=_data)
        print(res.text)
        _dis_val['id'] = json.loads(res.text)['data']['id']
        for _con_id,_con_val in _dis_val['constituency'].items():
            _data = {
                'name': _con_val['name'],
                'description': _con_val['description'],
                'link': _con_val['link'],
                'image': _con_val['image'],
                'district': _dis_val['id'],
            }
            res = requests.post(host+'/api/location/constituencies/', data=_data)
            print(res.text)
            # _con_val['id'] = json.loads(res.text)['data']['id']