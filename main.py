import nonebot
import json
from config import config
from os import path, mkdir

if not path.exists('.//config//whitelist.json'):
    with open('.//config//whitelist.json', 'w+', encoding='utf-8') as f:
        json.dump({'accept': True, 'whiteusers': [],
                   'whitegroups': []}, f, indent=4)

if not path.exists('.//data'):
    mkdir('.//data')

if __name__ == "__main__":
    nonebot.init(config)
    nonebot.load_plugins('.//applications//', 'applications')
    nonebot.run()
