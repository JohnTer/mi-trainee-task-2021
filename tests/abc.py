import pytest
from aiohttp import web

from pollapp.main import init_app


async def test_hello(aiohttp_client, loop):
    app = init_app()
    client = await aiohttp_client(app)
    resp = await client.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'Hello, world' in text
