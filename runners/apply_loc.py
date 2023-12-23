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
    print("Create State: ",res.status_code, _val['name'])
    _val['id'] = json.loads(res.text)['data']['id']
    for _dis_id,_dis_val in _val['districts'].items():
        try:des1 = _dis_val['description']
        except:des1 = None
        try:img1 = _dis_val['image']
        except:img1 = None
        try:link1 = _dis_val['link']
        except:link1 = None
        _data = {
            'state_id': _val['id'],
            'name': _dis_val['name'],
            'link': link1, 
            'description': des1,
            'image': img1,
            'state': _val['id'],
        }
        res = requests.post(host+'/api/location/districts/', data=_data)
        print(" -- Create District: ",res.status_code, _dis_val['name'])
        _dis_val['id'] = json.loads(res.text)['data']['id']
        for _con_id,_con_val in _dis_val['constituency'].items():
            try:des2 = _con_val['description']
            except:des2 = None
            try:img2 = _con_val['image']
            except:img2 = None
            try:link2 = _con_val['link']
            except:link2 = None
            _data = {
                'name': _con_val['name'],
                'description': des2,
                'link': link2,
                'image': img2,
                'district': _dis_val['id'],
            }
            res = requests.post(host+'/api/location/constituencies/', data=_data)
            print("    -- Create Constituency: ",res.status_code, _con_val['name'])
            # _con_val['id'] = json.loads(res.text)['data']['id']