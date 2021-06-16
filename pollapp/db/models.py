from sqlalchemy.dialects.postgresql import JSON

from . import db


class Poll(db.Model):
    __tablename__ = 'polls'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    answers = db.Column(JSON())
