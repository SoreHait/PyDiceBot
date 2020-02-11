from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession
from app_addon.json_operations import loadjson, dumpjson
from random import randint


@on_command('rep', only_to_me=False)
async def repeat(session: CommandSession):
    mode = session.get('mode')
    if mode == 'None':
        await session.send('请输入参数，请通过.help rep查看帮助')
    elif mode == 'Else':
        await session.send('未知参数，请通过.help rep查看帮助')
    elif mode == 'show':
        gid = session.ctx['group_id']
        data = loadjson(gid)
        try:
            rate = data['repRate']
        except Exception:
            await session.send('当前复读几率为0')
            return
        await session.send(f'当前复读机率为{rate}')
    elif mode == 'set':
        role = session.ctx['sender']['role']
        if role not in ['owner', 'admin']:
            await session.send('只有管理员或群主才可使用此命令')
            return
        rate = session.get('rate')
        try:
            rate = int(rate)
        except Exception:
            await session.send('请输入一个在0-100之间的数')
            return
        if 0 <= rate <= 100:
            gid = session.ctx['group_id']
            data = loadjson(gid)
            data['repRate'] = rate
            dumpjson(gid, data)
        else:
            await session.send('请输入一个在0-100之间的数')


@repeat.args_parser
async def _(session: CommandSession):
    mode = session.current_arg_text.split(' ')
    if session.current_arg_text == '':
        session.state['mode'] = 'None'
    elif mode[0] == 'set':
        session.state['mode'] = 'set'
        session.state['rate'] = mode[1]
    elif mode[0] == 'show':
        session.state['mode'] = 'show'
    else:
        session.state['mode'] = 'Else'


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    text = session.msg_text
    gid = session.ctx['group_id']
    data = loadjson(gid)
    try:
        rate = int(data['repRate'])
    except Exception:
        return
    if rate == 0:
        return
    else:
        if randint(0,99) == list(range(rate)):
            await session.send(text)