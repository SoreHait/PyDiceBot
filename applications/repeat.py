from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from app_addon.json_operations import loadjson, dumpjson
from random import random


@on_command('rep', aliases=('fudu', 'fd', '复读',), only_to_me=False)
async def repeat(session: CommandSession):
    arg = session.current_arg_text
    if arg == 'off':
        arg = 0
    try:
        rate = float(arg)
    except Exception:
        if arg == '':
            await session.send('请输入参数，请通过.help rep查看帮助')
        elif arg == 'show':
            gid = session.ctx['group_id']
            data = loadjson(gid)
            try:
                rate = data['repRate']
            except Exception:
                await session.send('当前复读几率为0%')
                return
            await session.send(f'当前复读机率为{rate}%')
        else:
            await session.send('未知参数，请通过.help rep查看帮助')
        return
    role = session.ctx['sender']['role']
    if role not in ['owner', 'admin']:
        await session.send('只有管理员或群主才可使用此命令')
        return
    if 0 <= rate <= 100:
        gid = session.ctx['group_id']
        data = loadjson(gid)
        data['repRate'] = rate
        dumpjson(gid, data)
        await session.send('设定成功')
    else:
        await session.send('请输入一个在0-100之间的数')


@on_command('sayagain')
async def sayagain(session: CommandSession):
    gid = session.ctx['group_id']
    data = loadjson(gid)
    try:
        rate = float(data['repRate']/100)
    except Exception:
        return
    if rate == 0.0:
        return
    else:
        text = session.current_arg
        if random() <= rate:
            await session.send(text)


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    text = session.msg_text
    return IntentCommand(100.0, 'sayagain', current_arg=text)
