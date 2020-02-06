from nonebot import on_command, CommandSession
from app_addon.json_operations import dumpjson, loadjson

@on_command('set', only_to_me=False)
async def setmode(session: CommandSession):
    mode = session.get('mode')
    if (mode in ['coc','dnd']) or (str(type(mode)) == "<class 'int'>" and 1 <= mode <= 1000):
        gid = session.ctx['group_id']
        data = loadjson(gid)
        data['mode'] = mode
        dumpjson(gid, data)
        await session.send('设定成功')
    else:
        await session.send('请将模式设定为coc，dnd或1-1000范围内的整数')

@setmode.args_parser
async def _(session: CommandSession):
    try:
        session.state['mode'] = int(session.current_arg_text)
    except Exception:
        session.state['mode'] = session.current_arg_text.lower()
    return