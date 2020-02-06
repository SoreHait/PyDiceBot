from nonebot import on_command, CommandSession
import json

def loadjson(gid):
    with open(f'.//data//{gid}.json', 'w+', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return {}
def dumpjson(gid, data):
    with open(f'.//data//{gid}.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

@on_command('nn', only_to_me=False)
async def name(session: CommandSession):
    name = session.get('name')
    uid = session.ctx['sender']['user_id']
    gid = session.ctx['group_id']
    data = loadjson(gid)
    data['name'][uid] = name
    dumpjson(gid, data)
    await session.send('设定成功')

@name.args_parser
async def _(session: CommandSession):
    session.state['name'] = session.current_arg_text 