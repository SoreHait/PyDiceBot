from nonebot import on_command, CommandSession
import sqlite3, random

@on_command('jrrp', aliases=('今日日批','今日人品'), only_to_me=False)
async def jrrp(session: CommandSession):
    uid = session.ctx['sender']['user_id']
    gid = session.ctx['group_id']
    db = sqlite3.connect(f'.//data//{gid}.db')
    c = db.cursor()
    try:
        c.execute(f"SELECT NAME FROM NAME WHERE UID='{uid}'")
    except Exception:
        c.execute(f"CREATE TABLE NAME (UID TEXT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL)")
        c.execute(f"SELECT NAME FROM NAME WHERE UID='{uid}'")
    fetch = c.fetchone()
    if str(fetch) == 'None':
        nickname = session.ctx['sender']['nickname']
    else:
        nickname = fetch[0]
    await session.send(f'{nickname}今天的人品值：{random.randint(1,100)}')