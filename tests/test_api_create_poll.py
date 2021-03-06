from http import HTTPStatus

import pytest

from aiohttp import http, web

from pollapp.app import init_app
from pollapp.db.models import Poll

CASES: list[tuple[dict, int]] = [
    ({
        'name': 'test',
        'answers': ['1', '2', '3']
    }, HTTPStatus.CREATED),

    ({
        'name': '',
        'answers': ['1', '2', '3']
    }, HTTPStatus.BAD_REQUEST),
    ({
        'name': 'test',
        'answers': []
    }, HTTPStatus.BAD_REQUEST),
    ({
        'answers': ['1', '2', '3']
    }, HTTPStatus.BAD_REQUEST),
    ({
        'name': 'test'

    }, HTTPStatus.BAD_REQUEST),
    ({
        'name': 'test',
        'answers': ['1', '2', '3'],
        'extra_field': 0
    }, HTTPStatus.BAD_REQUEST),
    ({
        'name': 123,
        'answers': ['1', '2', '3']
    }, HTTPStatus.BAD_REQUEST),
    ({
        'name': 'test',
        'answers': [1, 2, 3]
    }, HTTPStatus.BAD_REQUEST),
    ({
        'name': 'test',
        'answers': 123
    }, HTTPStatus.BAD_REQUEST),
]


@pytest.mark.parametrize('json_body,expected_status', CASES)
async def test_create_poll(aiohttp_client, loop, json_body, expected_status):
    app = init_app()
    client = await aiohttp_client(app)
    resp = await client.post('/users/createPoll', json=json_body)
    assert resp.status == expected_status
    await Poll.delete.where(True).gino.status()
