from nonebot import on_command, CommandSession
import random, sqlite3

@on_command('r', only_to_me=False)
async def dice(session: CommandSession):
    uid = session.ctx['sender']['user_id']
    gid = session.ctx['group_id']
    db = sqlite3.connect(f".//data//{gid}.db")
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
    if session.get('mode') == 'default':
        defaultdice = 100
        c.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND NAME='MODE'")
        if c.fetchone()[0] == 0:
            pass
        else:
            c.execute(f"SELECT * FROM MODE")
            mode = c.fetchone()[0]
            if mode == 'coc':
                pass
            elif mode == 'dnd':
                defaultdice = 20
            else:
                defaultdice = int(mode)
        output = f'{nickname}的D{defaultdice}的结果是：\n{random.randint(1,defaultdice)}'
        await session.send(output)
    elif session.get('mode') == 'INT':
        try:
            num = int(session.get('num'))
            output = f'{nickname}的D{num}的结果是：\n{random.randint(1,num)}'
            await session.send(output)
        except Exception:
            await session.send('参数不合法，用.help r查看帮助')
        
    elif session.get('mode') == 'D':
        times = int(session.get('times'))
        num = int(session.get('num'))
        temp = [str(random.randint(1,num)) for i in range(times)]
        equation = '+'.join(temp)
        if times != 1:
            output = f'{nickname}的{session.current_arg_text.upper()}的结果是：\n{equation}={eval(equation)}'
        elif times == 1:
            output = f'{nickname}的{session.current_arg_text.upper()}的结果是：\n{eval(equation)}'
        await session.send(output)
    db.commit()
    db.close()

@dice.args_parser
async def _(session: CommandSession):
    if session.current_arg_text == '':
        session.state['mode'] = 'default'
    elif 'D' in session.current_arg_text.upper():
        args = session.current_arg_text.upper().split('D',1)
        session.state['times'] = args[0]
        session.state['num'] = args[1]
        session.state['mode'] = 'D'
    else:
        session.state['mode'] = 'INT'
        session.state['num'] = session.current_arg_text
    return

@on_command('h', only_to_me=False)
async def diceprivate(session: CommandSession):
    uid = session.ctx['sender']['user_id']
    gid = session.ctx['group_id']
    db = sqlite3.connect(f".//data//{gid}.db")
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
    if session.get('mode') == 'default':
        defaultdice = 100
        c.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND NAME='MODE'")
        if c.fetchone()[0] == 0:
            pass
        else:
            c.execute(f"SELECT * FROM MODE")
            mode = c.fetchone()[0]
            if mode == 'coc':
                pass
            elif mode == 'dnd':
                defaultdice = 20
            else:
                defaultdice = int(mode)
        output = f'{nickname}的D{defaultdice}的结果是：\n{random.randint(1,defaultdice)}'
        await session.send(output, ensure_private=True)
    elif session.get('mode') == 'INT':
        num = 0
        try:
            num = int(session.get('num'))
            output = f'{nickname}的D{num}的结果是：\n{random.randint(1,num)}'
            await session.send(output, ensure_private=True)
        except Exception:
            await session.send('参数不合法，用.help h查看帮助', ensure_private=True)
    elif session.get('mode') == 'D':
        times = int(session.get('times'))
        num = int(session.get('num'))
        temp = [str(random.randint(1,num)) for i in range(times)]
        equation = '+'.join(temp)
        if times != 1:
            output = f'{nickname}的{session.current_arg_text.upper()}的结果是：\n{equation}={eval(equation)}'
        elif times == 1:
            output = f'{nickname}的{session.current_arg_text.upper()}的结果是：\n{eval(equation)}'
        await session.send(output, ensure_private=True)
    db.commit()
    db.close()

@diceprivate.args_parser
async def _(session: CommandSession):
    if session.current_arg_text == '':
        session.state['mode'] = 'default'
    elif 'D' in session.current_arg_text.upper():
        args = session.current_arg_text.upper().split('D',1)
        session.state['times'] = args[0]
        session.state['num'] = args[1]
        session.state['mode'] = 'D'
    else:
        session.state['mode'] = 'INT'
        session.state['num'] = session.current_arg_text
    return