import nonebot
from config import config

if __name__ == "__main__":
    nonebot.init(config)
    nonebot.load_plugins('.//applications//','applications')
    nonebot.run()