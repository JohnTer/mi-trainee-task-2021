from aiohttp import web

from pollapp.api.views import routes
from pollapp.db.models import db


async def create(app_):
    await db.gino.create_all()


def init_app(config_object: object):
    app = web.Application(middlewares=[db])

    db.init_app(app, dict(dsn=config_object.get_db_url()))
    app.router.add_routes(routes)
    app.on_startup.append(create)

    return app

