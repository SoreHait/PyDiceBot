from nonebot import on_command, CommandSession
import sqlite3

@on_command('nn', only_to_me=False)
async def name(session: CommandSession):
    name = session.get('name')
    uid = session.ctx['sender']['user_id']
    gid = session.ctx['group_id']
    db = sqlite3.connect(f".//data//{gid}.db")
    c = db.cursor()
    c.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND NAME='NAME'")
    if c.fetchone()[0] == 0:
        c.execute(f"CREATE TABLE NAME (UID TEXT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL)")
        c.execute(f"INSERT INTO NAME (UID,NAME) VALUES ('{uid}','{name}')")
    else:
        c.execute(f"SELECT COUNT(*) FROM NAME WHERE UID='{uid}'")
        if c.fetchone()[0] == 0:
            c.execute(f"INSERT INTO NAME (UID,NAME) VALUES ('{uid}','{name}')")
        else:
            c.execute(f"UPDATE NAME SET NAME='{name}' WHERE UID='{uid}'")
    db.commit()
    db.close()
    await session.send('设定成功')

@name.args_parser
async def _(session: CommandSession):
    session.state['name'] = session.current_arg_text 