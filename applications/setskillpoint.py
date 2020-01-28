from nonebot import on_command, CommandSession
import sqlite3

@on_command('st', only_to_me=False)
async def setsp(session: CommandSession):
    skpts = session.get('skpts')
    uid = session.ctx['sender']['user_id']
    gid = session.ctx['group_id']
    db = sqlite3.connect(f'.//data//{gid}.db')
    c = db.cursor()
    c.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND NAME='{uid}'")
    if c.fetchone()[0] == 0:
        c.execute(f"CREATE TABLE '{uid}' (SKNAME TEXT PRIMARY KEY NOT NULL, LVL TEXT NOT NULL)")
        for key in skpts.keys():
            c.execute(f"INSERT INTO '{uid}' (SKNAME,LVL) VALUES ('{key}','{skpts[key]}')")
    else:
        for key in skpts.keys():
            c.execute(f"SELECT COUNT(*) FROM '{uid}' WHERE SKNAME='{key}'")
            if c.fetchone()[0] == 0:
                c.execute(f"INSERT INTO '{uid}' (SKNAME,LVL) VALUES ('{key}','{skpts[key]}')")
            else:
                c.execute(f"UPDATE '{uid}' SET LVL='{skpts[key]}' WHERE SKNAME='{key}'")
    db.commit()
    db.close()
    await session.send('设定成功')

@setsp.args_parser
async def _(session: CommandSession):
    if session.current_arg_text == 'clr':
        session.state['mode'] = 'clr'
    else:
        rawtext = session.current_arg_text.upper()
        replacel = {
            '：':':',
            'STR':'力量',
            'DEX':'敏捷',
            'CON':'体质',
            'INT':'智力',
            '灵感':'智力',
            'WIS':'感知',
            'CHA':'魅力',
            'SIZ':'体型',
            'APP':'外貌',
            'POW':'意志',
            'EDU':'教育',
            'LUCK':'幸运',
        }
        for key in replacel.keys():
            rawtext = rawtext.replace(key,replacel[key])
        rawinput = rawtext.split(' ')
        skpts = {}
        for item in rawinput:
            sk = item.split(':')
            skname = sk[0]
            skpt = sk[1]
            skpts[skname] = skpt
        session.state['skpts'] = skpts
        return