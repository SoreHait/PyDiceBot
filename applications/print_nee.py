from nonebot import on_command, CommandSession


msg = '呐呐，桥都麻袋，这样子讲话有什么错吗？呐，告诉我啊。搜噶，米娜桑已经不喜欢了啊......真是冷酷的人呢。果咩纳塞，让你看到不愉快的东西了。像我这样的人，果然消失就好了呢。也许只有在二次元的世界里，才有真正的美好存在吧，呐？'

@on_command('ne', aliases=('nee', 'ね', '呐'), only_to_me=False)
async def printNee(session: CommandSession):
    await session.send(msg)
