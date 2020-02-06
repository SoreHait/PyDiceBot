from nonebot import on_command, CommandSession
import re
from app_addon.json_operations import dumpjson, loadjson

@on_command('st', only_to_me=False)
async def setsp(session: CommandSession):
    uid = session.ctx['sender']['user_id']
    gid = session.ctx['group_id']
    mode = session.get('mode')
    data = loadjson(gid)
    if mode == 'clr':
        try:
            del data[uid]
        finally:
            await session.send('删除成功')
    elif mode == 'change':
        changelist = session.get('changelist')
        for item in changelist:
            skname = re.search(r'.+?(?=(\d))',item).group()
            lvl = re.search(r'(\d)+',item).group()
            data[uid][skname] = lvl
        await session.send('设定成功')
    elif mode == 'shift':
        try:
            nickname = data['name'][uid]
        except Exception:
            nickname = session.ctx['sender']['nickname']
        shiftlist = session.get('shiftlist')
        try:
            data[uid]
        except Exception:
            await session.send(f'{nickname}未设定属性值')
            return
        output = []
        for item in shiftlist:
            skname = re.search(r'.+?(?=[\+\-\*\/])',item).group()
            try:
                oglvl = data[uid][skname]
            except Exception:
                output.append(f"{skname}：未设定原值")
                continue
            shiftlvl = re.search(r'[\+\-\*\/](\d)+',item).group()
            newlvl = eval(f"{oglvl}{shiftlvl}")
            data[uid][skname] = newlvl
            output.append(f"{skname}：{oglvl}{shiftlvl}={newlvl}")
        await session.send('{}的属性已更新：\n{}'.format(nickname, '\n'.join(output)))
    elif mode == 'del':
        for item in session.get('dellist'):
            try:
                del data[uid][item]
            finally:
                pass
        await session.send('删除成功')
    elif mode == 'show':
        try:
            nickname = data['name'][uid]
        except Exception:
            nickname = session.ctx['sender']['nickname']
        output = []
        for item in data[uid].keys():
            output.append(f'{item}:{data[uid][item]}')
        await session.send('{}的当前属性：\n{}'.format(nickname,'\n'.join(output)))
    dumpjson(gid, data)

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