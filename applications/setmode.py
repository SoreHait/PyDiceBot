from nonebot import on_command, CommandSession
import sqlite3

@on_command('set', only_to_me=False)
async def setmode(session: CommandSession):
    mode = session.get('mode')
    gid = session.get('groupid')
    db = sqlite3.connect('.//data//group.db')
    c = db.cursor()
    c.execute(f"SELECT GID FROM DATA WHERE GID={gid}")
    if len(c.fetchall()) == 0:
        c.execute(f"INSERT INTO DATA (GID,MODE) VALUES ('{gid}','{mode}')")
    else:
        c.execute(f"UPDATE DATA SET MODE='{mode}' WHERE GID={gid}")
    db.commit()
    db.close()
    await session.send('设定成功')

@setmode.args_parser
async def _(session: CommandSession):
    session.state['groupid'] = session.ctx['group_id']
    session.state['mode'] = session.current_arg_text
    return