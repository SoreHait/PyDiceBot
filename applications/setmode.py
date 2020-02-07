from nonebot import on_command, CommandSession
from app_addon.json_operations import dumpjson, loadjson

@on_command('set', only_to_me=False)
async def setmode(session: CommandSession):
    mode = session.get('mode')
    gid = session.ctx['group_id']
    if mode == 'clr':
        data = loadjson(gid)
        try:
            del data['mode']
        except Exception:
            pass
        await session.send('默认规则清除成功')
        dumpjson(gid, data)
    elif mode == 'show':
        data = loadjson(gid)
        try:
            currentmode = data['mode']
        except KeyError:
            await session.send('当前没有设定规则，默认使用coc规则')
            return
        try:
            currentmode = int(currentmode)
        except Exception:
            pass
        if currentmode in ['coc','dnd']:
            await session.send(f'当前规则是{currentmode}规则')
        else:
            await session.send(f'当前默认骰是{currentmode}')
    elif (mode in ['coc','dnd']) or (str(type(mode)) == "<class 'int'>" and 1 <= mode <= 1000):
        data = loadjson(gid)
        data['mode'] = mode
        dumpjson(gid, data)
        await session.send('设定成功')
    else:
        await session.send('请将模式设定为coc，dnd或1-1000范围内的整数')

@setmode.args_parser
async def _(session: CommandSession):
    if session.current_arg_text == 'show':
        session.state['mode'] = 'show'
    elif session.current_arg_text == 'clr':
        session.state['mode'] = 'clr'
    try:
        session.state['mode'] = int(session.current_arg_text)
    except Exception:
        session.state['mode'] = session.current_arg_text.lower()
    return