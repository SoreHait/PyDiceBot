from nonebot import on_request, RequestSession
import json


@on_request('group')
async def _(session: RequestSession):
    try:
        with open('.//config//whitelist.json', 'r', encoding='utf-8') as f:
            whitelist = json.load(f)
    except Exception:
        with open('.//config//whitelist.json', 'w+', encoding='utf-8') as f:
            json.dump({'accept': True, 'whiteusers': [],
                       'whitegroups': []}, f, indent=4)
        whitelist = {'accept': True, 'whiteusers': [], 'whitegroups': []}
    accept = whitelist['accept']
    whitelist_group = whitelist['whitegroups']
    whitelist_user = whitelist['whiteusers']
    if session.ctx['sub_type'] == 'invite' and accept:
        await session.approve()
    elif session.ctx['sub_type'] == 'invite' and session.ctx['group_id'] in whitelist_group:
        await session.approve()
    elif session.ctx['sub_type'] == 'invite' and session.ctx['user_id'] in whitelist_user:
        await session.approve()
    else:
        await session.reject()
