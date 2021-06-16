from aiohttp import web

from pollapp.api.views import routes
from pollapp.db.models import db


async def create(app_):
    await db.gino.create_all()


def init_app(config_object):
    app = web.Application(middlewares=[db])

    PG_URL = 'postgres://postgres:postgres@localhost/pollapp'
    db.init_app(app, dict(dsn=PG_URL))
    app.router.add_routes(routes)
    app.on_startup.append(create)

    return app

