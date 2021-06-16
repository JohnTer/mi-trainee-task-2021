from http import HTTPStatus

import pytest

from aiohttp import http, web

from pollapp.main import init_app
from pollapp.db.models import Poll

CASES_INVALID: list[tuple[dict, int]] = [
    ({

    }, HTTPStatus.BAD_REQUEST),

    ({
        'ext_field': None,
    }, HTTPStatus.BAD_REQUEST),

    ({
        'poll_id': 1
    }, HTTPStatus.BAD_REQUEST)
]

CASES_OK: list[tuple[dict, int]] = [
    ({
        'poll_id': None
    }, HTTPStatus.OK)
]

CASES_NOT_FOUND: list[tuple[dict, int]] = [
    ({
        'poll_id': '1'
    }, HTTPStatus.NOT_FOUND)
]


@pytest.mark.parametrize('json_body,expected_status', CASES_OK)
async def test_result_ok(aiohttp_client, loop, json_body, expected_status):
    app = init_app()
    client = await aiohttp_client(app)

    init_request_json_body: dict = {
        'name': 'test',
        'answers': ['1', '2', '3']
    }
    resp = await client.post('/users/createPoll', json=init_request_json_body)
    assert resp.status == HTTPStatus.CREATED
    poll_id: str = (await resp.json())['poll_id']

    result_request_json_body: dict = {
        'poll_id': poll_id,
        'choice': '1'
    }
    resp = await client.post('/users/poll', json=result_request_json_body)
    assert resp.status == expected_status

    json_body['poll_id'] = poll_id
    resp = await client.post('/users/getResult', json=json_body)
    assert resp.status == HTTPStatus.OK

    vote_count: int = (await resp.json())['answers']['1']
    assert vote_count == 1

    await Poll.delete.where(True).gino.status()


@pytest.mark.parametrize('json_body,expected_status', CASES_INVALID)
async def test_result_invalid(aiohttp_client, loop, json_body, expected_status):
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


@pytest.mark.parametrize('json_body,expected_status', CASES_NOT_FOUND)
async def test_result_not_found(aiohttp_client, loop, json_body, expected_status):
    app = init_app()
    client = await aiohttp_client(app)

    init_request_json_body: dict = {
        'name': 'test',
        'answers': ['1', '2', '3']
    }
    resp = await client.post('/users/createPoll', json=init_request_json_body)
    assert resp.status == HTTPStatus.CREATED
    poll_id: str = (await resp.json())['poll_id']

    result_request_json_body: dict = {
        'poll_id': poll_id,
        'choice': '1'
    }
    resp = await client.post('/users/poll', json=result_request_json_body)
    assert resp.status == HTTPStatus.OK

    resp = await client.post('/users/getResult', json=json_body)
    assert resp.status == expected_status

    await Poll.delete.where(True).gino.status()
