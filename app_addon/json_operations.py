import json
from os import path

def loadjson(fname):
    if not path.exists(f'.//data//{fname}.json'):
        with open(f'.//data//{fname}.json', 'w+', encoding='utf-8') as f:
            return {}
    else:
        with open(f'.//data//{fname}.json', 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except Exception:
                return {}

def dumpjson(fname, data):
    with open(f'.//data//{fname}.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, indent=4)