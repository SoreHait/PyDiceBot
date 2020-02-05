from nonebot import on_request, RequestSession

accept = False
whitelist_group = [
    1011692502,
    855596096
]
whitelist_user = [

]

@on_request('group')
async def _(session: RequestSession):
    if session.ctx['sub_type'] == 'invite' and accept:
        await session.approve()
    elif session.ctx['sub_type'] == 'invite' and session.ctx['group_id'] in whitelist_group:
        await session.approve()
    elif session.ctx['sub_type'] == 'invite' and session.ctx['user_id'] in whitelist_user:
        await session.approve()
    else:
        await session.reject()