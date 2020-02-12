from nonebot import on_command, CommandSession
from base64 import b64encode, b64decode


@on_command('b64', only_to_me=False)
async def b64conv(session: CommandSession):
    mode = session.get('mode')
    if mode == 'None':
        await session.send('请输入参数，输入.help b64查看帮助')
    elif mode == 'SyntaxError':
        await session.send('参数不足，输入.help b64查看帮助')
    elif mode == 'en':
        text = session.get('text').encode()
        await session.send(f'Base64加密后：{b64encode(text).decode()}')
    elif mode == 'de':
        code = session.get('text')
        try:
            text = b64decode(code).decode()
        except Exception:
            text = b64decode(code).decode('gbk')
        await session.send(f'Base64解密后：{text}')



@b64conv.args_parser
async def _(session: CommandSession):
    args = session.current_arg_text.split(' ', 1)
    if session.current_arg_text == '':
        session.state['mode'] = 'None'
    elif len(args) == 1:
        session.state['mode'] = 'SyntaxError'
    elif len(args) == 2:
        session.state['mode'] = args[0]
        session.state['text'] = args[1]
    return