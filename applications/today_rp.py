from nonebot import on_command, CommandSession
import json, random

def loadjson(gid):
    with open(f'.//data//{gid}.json', 'w+', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return {}

@on_command('jrrp', aliases=('今日日批','今日人品'), only_to_me=False)
async def jrrp(session: CommandSession):
    uid = session.ctx['sender']['user_id']
    gid = session.ctx['group_id']
    data = loadjson(gid)
    try:
        nickname = data['name'][uid]
    except Exception:
        nickname = session.ctx['sender']['nickname']
    await session.send(f'{nickname}今天的人品值：{random.randint(1,100)}')