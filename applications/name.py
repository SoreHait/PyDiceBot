from nonebot import on_command, CommandSession
from app_addon.json_operations import dumpjson, loadjson

@on_command('nn', only_to_me=False)
async def name(session: CommandSession):
    name = session.get('name')
    uid = str(session.ctx['sender']['user_id'])
    gid = session.ctx['group_id']
    data = loadjson(gid)
    try:
        data['name']
    except Exception:
        data['name'] = {}
    data['name'][uid] = name
    dumpjson(gid, data)
    await session.send('设定成功')

@name.args_parser
async def _(session: CommandSession):
    session.state['name'] = session.current_arg_text 