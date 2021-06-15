from aiohttp import web

from api.views import routes
from db.models import db

async def create(app_):
    await db.gino.create_all()

if __name__ == '__main__':
    app = web.Application(middlewares=[db])

    PG_URL = 'postgres://postgres:postgres@localhost/pollapp'
    db.init_app(app, dict(dsn=PG_URL))
    app.router.add_routes(routes)
    app.on_startup.append(create)
    web.run_app(app)