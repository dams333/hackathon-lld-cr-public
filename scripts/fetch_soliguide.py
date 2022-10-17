# this tool dump all entries from soliguide database by location

from sys import argv
import pandas as pd
import requests
import json

def dump_assos_by_location(location: str):
    url = 'https://api.prosoliguide.fr/new-search'
    headers = {
        'Authorization': 'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MzQ5OTgyN2FmZGI3NzgzOWEyNmY2MDMiLCJpYXQiOjE2NjU3Njc5MTYsImV4cCI6MTY5NzMwMzkxNn0.UMjmas1ZyJlaXSS8S90vqdr7j3x_suHJMqM4EUD4_Y4'
    }
    payload = {
        "location": {
            "geoType": "ville",
            "geoValue": location
        },
        'options': {
            'limit': 1000000000 # please don't look, please don't ask
        }
    }

    req = requests.post(url=url, headers=headers, json=payload)
    if req.status_code != 200:
        print(req.text)
        raise Exception(req)
    ret = json.loads(req.text)
    return ret['places']

ret = dump_assos_by_location(argv[1])

print(json.dumps(ret))
# print(ret['nbResults'])
# print(len(ret['places']))
