from sqlalchemy.dialects.postgresql import JSON

from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(), primary_key=True)
    nickname = db.Column(db.Integer())


class Poll(db.Model):
    __tablename__ = 'polls'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    answers = db.Column(JSON())
