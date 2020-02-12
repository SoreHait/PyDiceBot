from nonebot import on_command, CommandSession
from os import path, remove

@on_command('reset', only_to_me=False)
async def reset(session: CommandSession):
    gid = session.ctx['group_id']
    role = session.ctx['sender']['role']
    if role in ['owner', 'admin']:
        if path.exists(f'.//data//{gid}.json'):
            remove(f'.//data//{gid}.json')
        await session.send('重置完成')
    else:
        await session.send('只有管理员或群主才可使用此命令')