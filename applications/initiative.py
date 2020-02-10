from nonebot import on_command, CommandSession
from app_addon.json_operations import loadjson, dumpjson
import random


@on_command('ri')
async def rollInitiative(session: CommandSession):
    uid = str(session.ctx['sender']['user_id'])
    gid = session.ctx['group_id']
    data = loadjson(gid)
    try:
        nickname = data['name'][uid]
    except Exception:
        nickname = session.ctx['sender']['nickname']
    try:
        data['initiative']
    except Exception:
        data['initiative'] = {}
    try:
        data['initName']
    except Exception:
        data['initName'] = {}
    init = random.randint(1, 20)
    data['initiative'][uid] = init
    data['initName'][uid] = nickname
    dumpjson(gid, data)
    await session.send(f'{nickname}的先攻骰点：\nD20={init}')


@on_command('init')
async def readInitiative(session: CommandSession):
    gid = session.ctx['group_id']
    data = loadjson(gid)
    try:
        initiative = data['initiative']
    except KeyError:
        await session.send('没有先攻骰点数据')
        return
    initiative = sorted(initiative.items(),
                        key=lambda item: item[1], reverse=True)
    output = []
    i = 1
    for item in initiative:
        try:
            nickname = data['name'][item[0]]
        except Exception:
            nickname = data['initName'][item[0]]
        output.append(f'{i}.{nickname} {item[1]}')
        i += 1
    await session.send('先攻顺序：\n{}'.format('\n'.join(output)))
