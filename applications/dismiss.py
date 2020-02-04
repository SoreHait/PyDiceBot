from nonebot import on_command, CommandSession
from os import path, remove

@on_command('dismiss', only_to_me=False)
async def dismiss(session: CommandSession):
    gid = int(session.ctx['group_id'])
    print(gid)
    bot = session.bot
    await session.send('正在清理本群数据库')
    if path.exists(f'.//data//{gid}.db'):
        remove(f'.//data//{gid}.db')
    await session.send('bot将退出群聊')
    await bot.set_group_leave(group_id=gid)