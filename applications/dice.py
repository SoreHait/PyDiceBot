from nonebot import on_command, CommandSession
import random
from app_addon.json_operations import loadjson

modifier = [
    '-5','-4','-4','-3','-3','-2','-2','-1','-1','+0','+0','+1','+1','+2','+2','+3','+3','+4','+4','+5','+5','+6','+6','+7','+7','+8','+8','+9','+9','+10'
]

@on_command('r', only_to_me=False)
async def dice(session: CommandSession):
    uid = session.ctx['sender']['user_id']
    gid = session.ctx['group_id']
    data = loadjson(gid)
    try:
        nickname = data['name'][uid]
    except Exception:
        nickname = session.ctx['sender']['nickname']
    if session.get('mode') == 'default':
        defaultdice = 100
        try:
            mode = data['mode']
        except Exception:
            mode = 'coc'
        if mode == 'dnd':
            defaultdice = 20
        else:
            defaultdice = int(mode)
        await session.send(f'{nickname}的D{defaultdice}的结果是：\n{random.randint(1,defaultdice)}')
    elif session.get('mode') == 'INT':
        try:
            num = int(session.get('num'))
            await session.send(f'{nickname}的D{num}的结果是：\n{random.randint(1,num)}')
        except Exception:
            await session.send('参数不合法，用.help r查看帮助')
    elif session.get('mode') == 'D':
        times = int(session.get('times'))
        num = int(session.get('num'))
        if not (times > 0 and num > 0):
            await session.send('参数不合法')
            return
        temp = [str(random.randint(1,num)) for i in range(times)]
        expression = '+'.join(temp)
        if times != 1:
            output = f'{nickname}的{session.current_arg_text.upper()}的结果是：\n{expression}={eval(expression)}'
        elif times == 1:
            output = f'{nickname}的{session.current_arg_text.upper()}的结果是：\n{eval(expression)}'
        await session.send(output)

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
    data = loadjson(gid)
    try:
        nickname = data['name'][uid]
    except Exception:
        nickname = session.ctx['sender']['nickname']
    if session.get('mode') == 'default':
        defaultdice = 100
        try:
            mode = data['mode']
        except Exception:
            mode = 'coc'
        if mode == 'dnd':
            defaultdice = 20
        else:
            defaultdice = int(mode)
        await session.send(f'{nickname}的D{defaultdice}的结果是：\n{random.randint(1,defaultdice)}',ensure_private=True)
    elif session.get('mode') == 'INT':
        try:
            num = int(session.get('num'))
            await session.send(f'{nickname}的D{num}的结果是：\n{random.randint(1,num)}',ensure_private=True)
        except Exception:
            await session.send('参数不合法，用.help h查看帮助',ensure_private=True)
    elif session.get('mode') == 'D':
        times = int(session.get('times'))
        num = int(session.get('num'))
        if not (times > 0 and num > 0):
            await session.send('参数不合法',ensure_private=True)
            return
        temp = [str(random.randint(1,num)) for i in range(times)]
        expression = '+'.join(temp)
        if times != 1:
            output = f'{nickname}的{session.current_arg_text.upper()}的结果是：\n{expression}={eval(expression)}'
        elif times == 1:
            output = f'{nickname}的{session.current_arg_text.upper()}的结果是：\n{eval(expression)}'
        await session.send(output,ensure_private=True)

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

@on_command('rc', aliases=('ra',), only_to_me=False)
async def rc(session: CommandSession):
    mode = session.get('mode')
    if mode == 'Error':
        await session.send('指令格式有误，请通过[.help rc]查看帮助')
        return
    gid = session.ctx['group_id']
    uid = session.ctx['sender']['user_id']
    data = loadjson(gid)
    if mode == 'Normal':
        try:
            mode = data['mode']
        except Exception:
            mode = 'coc'
    try:
        nickname = data['name'][uid]
    except Exception:
        nickname = session.ctx['sender']['nickname']
    if mode == 'dnd':
        mod = ''
        skname = session.get('skname')
        try:
            lvl = data[uid][skname]
        except Exception:
            await session.send('未设定此属性值')
            return
        if 1 <= lvl <= 30:
            mod = modifier[lvl]
        elif lvl < 1:
            mod = '-5'
        elif lvl > 30:
            mod = '+10'
        roll = str(random.randint(1,20))
        expression = ''.join([roll,mod])
        await session.send(f'{nickname}的{skname}检定的结果是：\n{expression}={eval(expression)}')
    else:
        skname = session.get('skname')
        lvl = 0
        if mode == 'custom':
            lvl = session.get('lvl')
        else:
            try:
                lvl = data[uid][skname]
            except Exception:
                await session.send('未设定此属性值')
                return
        roll = random.randint(1,100)
        out = ''
        if roll <= 5:
            out = '大成功'
        elif roll >= 95:
            out = '大失败'
        elif lvl/2 <= roll < lvl:
            out = '成功'
        elif lvl/5 <= roll < lvl/2:
            out = '困难成功'
        elif roll < lvl/5:
            out = '极难成功'
        else:
            out = '失败'
        await session.send(f'{nickname}的{skname}检定的结果是：\n{roll}/{lvl}，{out}')

@rc.args_parser
async def _(session: CommandSession):
    rawtext = session.current_arg_text.upper()
    replacel = {
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
    }
    for key in replacel.keys():
        rawtext = rawtext.replace(key,replacel[key])
    args = rawtext.split(' ')
    length = len(args)
    if length == 1:
        session.state['mode'] = 'Normal'
        session.state['skname'] = args[0]
    elif length == 2:
        try:
            session.state['lvl'] = int(args[1])
            session.state['skname'] = args[0]
            session.state['mode'] = 'custom'
        except Exception:
            session.state['mode'] = 'Error'
    else:
        session.state['mode'] = 'Error'