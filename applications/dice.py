from nonebot import on_command, CommandSession
import random, re

@on_command('r')
async def dice(session: CommandSession):
    times = int(session.get('times'))
    num = int(session.get('num'))
    temp = [str(random.randint(1,num)) for i in range(times)]
    equation = '+'.join(temp)
    output = f'.r {times}d{num}的结果是：\n{equation}={eval(equation)}'
    await session.send(output)

@dice.args_parser
async def _(session: CommandSession):
    args = session.current_arg_text.strip().split('d')
    session.state['times'] = args[0]
    session.state['num'] = args[1]
    return