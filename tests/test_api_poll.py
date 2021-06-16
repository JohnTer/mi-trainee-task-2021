from http import HTTPStatus

import pytest

from aiohttp import http, web

from pollapp.app import init_app
from pollapp.db.models import Poll

CASES_INVALID: list[tuple[dict, int]] = [
    ({
        'poll_id': None,
        'choice': 1
    }, HTTPStatus.BAD_REQUEST),

    ({
        'poll_id': None,
    }, HTTPStatus.BAD_REQUEST),

    ({
        'answer': '1'
    }, HTTPStatus.BAD_REQUEST),

    ({
        'poll_id': None,
        'choice': '1',
        'extra_field': ''
    }, HTTPStatus.BAD_REQUEST),
]

CASES_OK: list[tuple[dict, int]] = [
    ({
        'poll_id': None,
        'choice': '1'
    }, HTTPStatus.OK)
]

CASES_NOT_FOUND: list[tuple[dict, int]] = [
    ({
        'poll_id': '1',
        'choice': '1'
    }, HTTPStatus.NOT_FOUND)
]


@pytest.mark.parametrize('json_body,expected_status', CASES_OK)
async def test_poll_ok(aiohttp_client, loop, json_body, expected_status):
    app = init_app()
    client = await aiohttp_client(app)

    init_request_json_body: dict = {
        'name': 'test',
        'answers': ['1', '2', '3']
    }
    resp = await client.post('/users/createPoll', json=init_request_json_body)
    assert resp.status == HTTPStatus.CREATED
    poll_id: str = (await resp.json())['poll_id']

    json_body['poll_id'] = poll_id
    resp = await client.post('/users/poll', json=json_body)
    assert resp.status == expected_status

    result_request_json_body: dict = {
        'poll_id': poll_id
    }
    resp = await client.post('/users/getResult', json=result_request_json_body)
    assert resp.status == HTTPStatus.OK

    vote_count: int = (await resp.json())['answers']['1']
    assert vote_count == 1

    await Poll.delete.where(True).gino.status()


@pytest.mark.parametrize('json_body,expected_status', CASES_INVALID)
async def test_poll_invalid(aiohttp_client, loop, json_body, expected_status):
    app = init_app()
    client = await aiohttp_client(app)

    init_request_json_body: dict = {
        'name': 'test',
        'answers': ['1', '2', '3']
    }
    resp = await client.post('/users/createPoll', json=init_request_json_body)
    assert resp.status == HTTPStatus.CREATED
    poll_id: str = (await resp.json())['poll_id']

    if 'poll_id' in json_body:
        json_body['poll_id'] = poll_id
    resp = await client.post('/users/poll', json=json_body)
    assert resp.status == expected_status

    await Poll.delete.where(True).gino.status()


@pytest.mark.parametrize('json_body,expected_status', CASES_NOT_FOUND)
async def test_poll_not_found(aiohttp_client, loop, json_body, expected_status):
    app = init_app()
    client = await aiohttp_client(app)

    init_request_json_body: dict = {
        'name': 'test',
        'answers': ['1', '2', '3']
    }
    resp = await client.post('/users/createPoll', json=init_request_json_body)
    assert resp.status == HTTPStatus.CREATED

    resp = await client.post('/users/poll', json=json_body)
    assert resp.status == expected_status

    await Poll.delete.where(True).gino.status()
