from nonebot import on_command, CommandSession
from app_addon.json_operations import loadjson, dumpjson
import random


@on_command('ri', only_to_me=False)
async def rollInitiative(session: CommandSession):
    shift = session.get('shift')
    try:
        shiftint = int(shift)
    except Exception:
        if shift != '':
            await session.send('请输入一个加/减法算式')
            return
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
    data['initName'][uid] = nickname
    if shift == '':
        data['initiative'][uid] = init
        await session.send(f'{nickname}的先攻骰点：\nD20={init}')
    else:
        data['initiative'][uid] = init + shiftint
        if str(shiftint) == shift and not '-' in shift:
            await session.send(f'{nickname}的先攻骰点：\nD20+调整值={str(init)}+{shift}={init+shiftint}')
        else:
            await session.send(f'{nickname}的先攻骰点：\nD20+调整值={str(init)}{shift}={init+shiftint}')
    dumpjson(gid, data)


@rollInitiative.args_parser
async def _(session: CommandSession):
    if session.current_arg_text == '':
        session.state['shift'] = ''
    elif session.current_arg_text != '':
        session.state['shift'] = session.current_arg_text
    return


@on_command('init', only_to_me=False)
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
