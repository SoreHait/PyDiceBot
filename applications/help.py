from nonebot import on_command, CommandSession

@on_command('help', only_to_me=False)
async def help(session: CommandSession):
    keyword = session.get('keyword')
    if keyword == '':
        await session.send(
        'PyDiceBot\n'
        'Developed by SoreHait\n'
        'Support: HoshinoYuki\n'
        'Version: [Early Access] 0.1.3\n'
        '每个群的配置不通用，玩家需要单独在每个群内设定角色属性及角色名称\n'
        '重要！直接把本bot踢出次数过多会导致bot被封号\n'
        '请使用 [.dismiss] 让bot自己退群\n'
        '请使用 [.help 指令] 查看所有指令\n'
        '请使用 [.help [指令名称]] 查看该指令帮助\n'
        '如：.help r\n'
        '---已完成功能---\n'
        '.r .h .st .nn .set\n'
        '.dismiss .jrrp .rc/ra\n'
        '---未完成功能---\n'
        '.rules .coc .dnd\n'
        '.sc .en .ri.init\n'
        '.draw .deck'
        )
    elif keyword == 'st':
        await session.send(
        '设置角色属性：.st [属性名称][属性数值]\n'
        '属性名称与属性数值间无空格，设置多个属性时每项用空格分隔\n'
        '允许在已有属性上进行四则运算操作，但不可与设定属性混用\n'
        '例：.st 力量20 敏捷20\n'
        '.st 力量+10 敏捷-10\n'
        '错误例子：.st 力量10 敏捷+10\n'
        '删除角色属性：.st del [属性名称]\n'
        '删除多个属性时每项用空格分隔\n'
        '例：.st del 力量 敏捷\n'
        '查看角色属性：.st show\n'
        '删除角色卡：.st clr'
        )
    elif keyword == 'r':
        await session.send(
        '掷骰：.r [骰子个数]d[骰子面数]\n'
        '不加参数视为掷一个默认骰\n'
        '范围：骰子个数1-100，骰子面数1-1000\n'
        '暗骰指令：.h'
        )
    elif keyword == 'h':
        await session.send(
        '使用方式同.r\n'
        '掷骰结果将私聊发送给掷骰人'
        )
    elif keyword == 'nn':
        await session.send(
        '设置角色名称：.nn [角色名称]'
        )
    elif keyword == 'set':
        await session.send(
        '设置房间骰子模式：.set [coc/dnd/1-1000的整数]'
        )
    elif keyword == 'jrrp':
        await session.send(
        '别问，问就自己试试'
        )
    elif keyword == 'dismiss':
        await session.send(
        '退群并删除本群数据库\n'
        '请注意，删除数据库操作不可逆'
        )
    elif keyword == 'rc':
        await session.send(
        '进行属性检定：.rc [属性名称]\n'
        '进行任意检定：.rc [任意事件] [数值]\n'
        )
    elif keyword == 'ra':
        await session.send(
        '进行属性检定：.ra [属性名称]\n'
        '进行任意检定：.ra [任意事件] [数值]\n'
        )

@help.args_parser
async def _(session: CommandSession):
    session.state['keyword'] = session.current_arg_text