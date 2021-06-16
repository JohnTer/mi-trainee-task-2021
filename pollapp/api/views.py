from typing import Optional
from uuid import uuid4

from aiohttp import web
from aiohttp_validate import validate

from pollapp.db.models import Poll

routes = web.RouteTableDef()


@routes.post('/users/getResult')
@validate(request_schema={
    "type": "object",
    "properties": {
            "poll_id": {"type": "string", "format": "uuid"},
    },
    "required": ["poll_id"],
    "additionalProperties": False
})
async def get_result(raw_poll_data: dict[str, str], request: web.Request) -> web.Response:
    poll_id: str = raw_poll_data['poll_id']
    poll: Optional[Poll] = await Poll.query.where(Poll.id == poll_id).gino.first()
    if poll is None:
        return web.json_response({'error': 'Poll does not exist'}, status=404)
    return web.json_response({'name': poll.name, 'answers': poll.answers})


@routes.post('/users/poll')
@validate(request_schema={
    "type": "object",
    "properties": {
            "poll_id": {"type": "string", "format": "uuid"},
            "choice": {"type": "string"},
    },
    "required": ["poll_id", "choice"],
    "additionalProperties": False
})
async def poll(raw_poll_data: dict[str, str], request: web.Request) -> web.Response:
    poll_id: str = raw_poll_data['poll_id']
    choice: str = raw_poll_data['choice']

    poll: Optional[Poll] = await Poll.query.where(Poll.id == poll_id).gino.first()
    if poll is None:
        return web.json_response({'error': 'Poll does not exist'}, status=404)

    answers: dict[str, str] = poll.answers
    if choice not in answers:
        return web.json_response({'error': 'Answer does not exist'}, status=400)

    answers[choice] += 1
    await poll.update(answers=answers).apply()
    return web.json_response({'status': 'ok'})


@routes.post('/users/createPoll')
@validate(request_schema={
    "type": "object",
    "properties": {
            "name": {"type": "string", "minLength": 1},
            "answers": {"type": "array", "items": {
                "type": "string"
            },"minItems": 1},
    },
    "required": ["name", "answers"],
    "additionalProperties": False
})
async def create_poll(raw_poll_data: dict[str, str], request: web.Request) -> web.Response:
    poll_id: str = str(uuid4())
    name: str = raw_poll_data['name']
    answer_list: list[str] = raw_poll_data['answers']

    answers: dict[str, str] = {answer: 0 for answer in answer_list}

    await Poll.create(id=poll_id, name=name, answers=answers)
    return web.json_response({'poll_id': poll_id}, status=201)
