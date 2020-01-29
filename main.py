import nonebot
from config import config
from os import path, mkdir

if not path.exists('.//data'):
    mkdir('.//data')

if __name__ == "__main__":
    nonebot.init(config)
    nonebot.load_plugins('.//applications//','applications')
    nonebot.run()