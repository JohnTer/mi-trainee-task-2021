from aiohttp import web

from db.models import Poll

routes = web.RouteTableDef()


@routes.post('/users/getResult')
async def get_user(request):
    raw_poll_id_data: dict[str, str] = await request.json()
    poll_id: str = raw_poll_id_data['poll_id']
    poll = await Poll.query.where(Poll.id == poll_id).gino.first()
    if poll is None:
        return web.json_response({'err': 'Poll does not exist', 'code': 404})
    else:
        return web.json_response({})



def init_app(app):
    app.router.add_routes(routes)
