from nonebot import on_command, CommandSession
from json import load

@on_command('help', only_to_me=False)
async def help(session: CommandSession):
    keyword = session.get('keyword')
    with open('.//app_addon//helpPages.json', 'r', encoding='utf-8') as f:
        helpPages = load(f)
    try:
        helpText = helpPages[keyword]
    except KeyError:
        helpText = '无此帮助页'
    await session.send(helpText)

@help.args_parser
async def _(session: CommandSession):
    session.state['keyword'] = session.current_arg_text