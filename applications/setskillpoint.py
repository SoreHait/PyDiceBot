from nonebot import on_command, CommandSession
import sqlite3, re

@on_command('st', only_to_me=False)
async def setsp(session: CommandSession):
    uid = session.ctx['sender']['user_id']
    gid = session.ctx['group_id']
    db = sqlite3.connect(f'.//data//{gid}.db')
    mode = session.get('mode')
    c = db.cursor()
    if mode == 'clr':
        c.execute(f"DELETE FROM '{uid}'")
        await session.send('删除成功')
    elif mode == 'change':
        changelist = session.get('changelist')
        c.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND NAME='{uid}'")
        if c.fetchone()[0] == 0:
            c.execute(f"CREATE TABLE '{uid}' (SKNAME TEXT PRIMARY KEY NOT NULL, LVL TEXT NOT NULL)")
            for item in changelist:
                skname = re.search(r'.+?(?=(\d))',item).group()
                lvl = re.search(r'(\d)+',item).group()
                c.execute(f"INSERT INTO '{uid}' (SKNAME,LVL) VALUES ('{skname}','{lvl}')")
        else:
            for item in changelist:
                skname = re.search(r'.+?(?=(\d))',item).group()
                lvl = re.search(r'(\d)+',item).group()
                c.execute(f"SELECT COUNT(*) FROM '{uid}' WHERE SKNAME='{skname}'")
                if c.fetchone()[0] == 0:
                    c.execute(f"INSERT INTO '{uid}' (SKNAME,LVL) VALUES ('{skname}','{lvl}')")
                else:
                    c.execute(f"UPDATE '{uid}' SET LVL='{lvl}' WHERE SKNAME='{skname}'")
        await session.send('设定成功')
    elif mode == 'shift':
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
        shiftlist = session.get('shiftlist')
        c.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND NAME='{uid}'")
        if c.fetchone()[0] == 0:
            await session.send(f'{nickname}未设定属性值')
        else:
            output = []
            for item in shiftlist:
                skname = re.search(r'.+?(?=[\+\-\*\/])',item).group()
                c.execute(f"SELECT COUNT(*) FROM '{uid}' WHERE SKNAME='{skname}'")
                if c.fetchone()[0] == 0:
                    output.append(f"{skname}：未设定原值")
                else:
                    c.execute(f"SELECT LVL FROM '{uid}' WHERE SKNAME='{skname}'")
                    oglvl = str(c.fetchone()[0])
                    shiftlvl = re.search(r'[\+\-\*\/](\d)+',item).group()
                    newlvl = eval(f"{oglvl}{shiftlvl}")
                    c.execute(f"UPDATE '{uid}' SET LVL='{newlvl}' WHERE SKNAME='{skname}'")
                    output.append(f"{skname}：{oglvl}{shiftlvl}={newlvl}")
            await session.send('{}的属性已更新：\n{}'.format(nickname, '\n'.join(output)))
    elif mode == 'del':
        for item in session.get('dellist'):
            c.execute(f"DELETE FROM '{uid}' WHERE SKNAME='{item}'")
        await session.send('删除成功')
    elif mode == 'show':
        c.execute(f"SELECT NAME FROM NAME WHERE UID='{uid}'")
        fetch = c.fetchone()
        if str(fetch) == 'None':
            nickname = session.ctx['sender']['nickname']
        else:
            nickname = fetch[0]
        c.execute(f"SELECT * FROM '{uid}'")
        output = []
        for item in c.fetchall():
            output.append(f'{item[0]}:{item[1]}')
        await session.send('{}的当前属性：\n{}'.format(nickname,'\n'.join(output)))
    db.commit()
    db.close()

@setsp.args_parser
async def _(session: CommandSession):
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
        'HP':'生命值',
        'MP':'魔力值',
        'SAN':'理智值',
        '侦查':'侦察',
        '＋':'+',
        '－':'-',
        '×':'*',
        'X':'*',
        '÷':'/',
    }
    for key in replacel.keys():
        rawtext = rawtext.replace(key,replacel[key])
    if session.current_arg_text == 'clr':
        session.state['mode'] = 'clr'
    elif session.current_arg_text == 'show':
        session.state['mode'] = 'show'
    elif str(re.search(r'[\+\-\*\/]',rawtext)) != 'None':
        session.state['mode'] = 'shift'
        session.state['shiftlist'] = rawtext.split(' ')
    elif session.current_arg_text.split(' ',1)[0] == 'del':
        session.state['mode'] = 'del'
        session.state['dellist'] = rawtext.split(' ')[1:]
    else:
        session.state['mode'] = 'change'
        session.state['changelist'] = rawtext.split(' ')
    return