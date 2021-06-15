from typing import Optional
from uuid import uuid4
from aiohttp import web

from db.models import Poll

routes = web.RouteTableDef()


@routes.post('/users/getResult')
async def get_result(request):
    raw_poll_id_data: dict[str, str] = await request.json()
    poll_id: str = raw_poll_id_data['poll_id']
    poll = await Poll.query.where(Poll.id == poll_id).gino.first()
    if poll is None:
        return web.json_response({'err': 'Poll does not exist', 'code': 404})

    return web.json_response({'name': poll.name, 'answers': poll.answers})


@routes.post('/users/poll')
async def poll(request):
    raw_poll_data: dict[str, str] = await request.json()
    poll_id: str = raw_poll_data['poll_id']
    choice: str = raw_poll_data['choice']

    poll: Optional[Poll] = await Poll.query.where(Poll.id == poll_id).gino.first()
    if poll is None:
        return web.json_response({'err': 'Poll does not exist', 'code': 404}, status=404)

    answers: dict[str, str] = poll.answers
    if choice not in answers:
        return web.json_response({'err': 'Answer does not exist', 'code': 400}, status=400)

    answers[choice] += 1
    await poll.update(answers=answers).apply()
    return web.json_response({'status': 'ok'})


@routes.post('/users/createPoll')
async def create_poll(request):
    raw_poll_data: dict[str, str] = await request.json()

    poll_id: str = str(uuid4())
    name: str = raw_poll_data['name']
    answer_list: list[str] = raw_poll_data['answers']

    answers: dict[str, str] = {answer: 0 for answer in answer_list}

    await Poll.create(id=poll_id, name=name, answers=answers)
    return web.json_response({'poll_id': poll_id}, status=201)


def init_app(app):
    app.router.add_routes(routes)
