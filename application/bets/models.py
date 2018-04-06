from application import db


class Bet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Integer, nullable = False)
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable = False)
    contestparticipant_id = db.Column(db.Integer, db.ForeignKey('contestparticipant.id'))

    def __init__(self, amount, account_id, contestparticipant_id):
        self.amount = amount
        self.account_id = account_id
        self.contestparticipant_id = contestparticipant_id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(3000), nullable = False)
    like = db.Column(db.Boolean, nullable = False)
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable = False)
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.id'), nullable = False)

    def __init__(self, text, like, account_id, contest_id):
        self.text = text
        self.like = _like
        self.account_id = account_id
        self.contest_id = contest_id


class Contest(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(144), nullable = False)
    description = db.Column(db.String(3000), nullable = False)
    approved = db.Column(db.Boolean, nullable = False)
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable = False)
    winner_id = db.Column(db.Integer, db.ForeignKey('contestparticipant.id'))

    def __init__(self, name, description, account_id):
        self.name = name
        self.description = description
        self.approved = False
        self.account_id = account_id


class ContestParticipant(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.id'), nullable = False)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'))

    def __init__(self, contest_id, participant_id):
        self.contest_id = contest_id
        self.participant_id = participant_id


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(144), nullable = False)
    description = db.Column(db.String(3000), nullable = False)
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())

    def __init__(self, name, description):
        self.name = name
        self.description = description


class OneTimePassword(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    password = db.Column(db.String(6), nullable = False)
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable = False)

    def __init__(self, password, account_id):
        self.password = password
        self.account_id = account_id

