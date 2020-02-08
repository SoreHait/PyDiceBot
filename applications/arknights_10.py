from nonebot import on_command, CommandSession
import random
from app_addon.json_operations import loadjson
from json import load

@on_command('draw', aliases=('方舟十连',), only_to_me=False)
async def draw10(session: CommandSession):
    uid = str(session.ctx['sender']['user_id'])
    gid = session.ctx['group_id']
    data = loadjson(gid)
    try:
        nickname = data['name'][uid]
    except Exception:
        nickname = session.ctx['sender']['nickname']
    try:
        with open('.//app_addon//arknights_operators.json', 'r', encoding='utf-8') as f:
            operators = load(f)
    except Exception:
        await session.send('干员数据库读取错误')
        return
    output = []
    stars = [random.randint(1,100) for i in range(10)]
    for i in stars:
        if 1 <= i <= 40:
            op = random.choice(operators['3'])
            output.append(f'【⭐⭐⭐】{op}')
        elif 41 <= i <= 90:
            op = random.choice(operators['4'])
            output.append(f'【⭐⭐⭐⭐】{op}')
        elif 91 <= i <= 98:
            op = random.choice(operators['5'])
            output.append(f'【⭐⭐⭐⭐⭐】{op}')
        elif i in [99,100]:
            op = random.choice(operators['6'])
            output.append(f'【⭐⭐⭐⭐⭐⭐】{op}')
    await session.send('{}的方舟十连抽出了：\n{}'.format(nickname, '\n'.join(output)))