from nonebot import on_command, CommandSession
import random

@on_command('r', only_to_me=False)
async def dice(session: CommandSession):
    times = int(session.get('times'))
    num = int(session.get('num'))
    temp = [str(random.randint(1,num)) for i in range(times)]
    equation = '+'.join(temp)
    if times != 1:
        output = f'{session.ctx["raw_message"]}的结果是：\n{equation}={eval(equation)}'
    elif times == 1:
        output = f'{session.ctx["raw_message"]}的结果是：\n{eval(equation)}'
    await session.send(output)

@dice.args_parser
async def _(session: CommandSession):
    args = session.current_arg_text.strip().split('d')
    session.state['times'] = args[0]
    session.state['num'] = args[1]
    return