from nonebot import on_command, CommandSession
import sqlite3

@on_command('set', only_to_me=False)
async def setmode(session: CommandSession):
    mode = session.get('mode')
    if (mode in ['coc','dnd']) or (str(type(mode)) == "<class 'int'>" and 1 <= mode <= 1000):
        gid = session.ctx['group_id']
        db = sqlite3.connect(f'.//data//{gid}.db')
        c = db.cursor()
        c.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND NAME='MODE'")
        if c.fetchone()[0] == 0:
            c.execute(f"CREATE TABLE MODE (MODE TEXT PRIMARY KEY NOT NULL)")
            c.execute(f"INSERT INTO MODE (MODE) VALUES ('{mode}')")
        else:
            c.execute(f"DELETE FROM MODE")
            c.execute(f"INSERT INTO MODE (MODE) VALUES ('{mode}')")
        db.commit()
        db.close()
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