from application import db
from application.models import Base
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


event_participant = Table('eventParticipant', Base.metadata,
        Column('event_id', Integer, ForeignKey('event.id')),
        Column('participant_id', Integer, ForeignKey('participant.id'))
)


class Bet(Base):
    amount = db.Column(db.Integer, nullable = False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable = False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable = False)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable = False)

    def __init__(self, amount, account_id, event_id, participant_id):
        self.amount = amount
        self.account_id = account_id
        self.event_id = event_id
        self.participant_id = participant_id


class Comment(Base):
    text = db.Column(db.String(3000), nullable = False)
    like = db.Column(db.Boolean)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __init__(self, text):
        self.text = text


class Event(Base):
    name = db.Column(db.String(144), nullable = False)
    description = db.Column(db.String(3000), nullable = False)
    approved = db.Column(db.Boolean)
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    creator = db.Column(db.Integer, db.ForeignKey('account.id'))
    winner = db.Column(db.Integer, db.ForeignKey('participant.id'))
    participants = relationship('Participant', secondary=event_participant, backref='events')

    def __init__(self, name, description, account_id):
        self.name = name
        self.description = description
        self.approved = False
        self.account_id = account_id


class OneTimePassword(Base):
    password = db.Column(db.String(6), nullable = False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable = False)

    def __init__(self, password, account_id):
        self.password = password
        self.account_id = account_id


class Participant(Base):
    name = db.Column(db.String(144), nullable = False)
    description = db.Column(db.String(3000), nullable = False)

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Role(Base):
    role = db.Column(db.String(32), nullable = False)

    def __init__(self, role):
        self.role = role
