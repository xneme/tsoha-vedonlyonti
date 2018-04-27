from sqlalchemy.ext.hybrid import hybrid_property
from application import bcrypt, db
from application.models import Base
from sqlalchemy.sql import text
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


account_role = Table('accountRole', Base.metadata,
        Column('account_id', Integer, ForeignKey('account.id')),
        Column('role_id', Integer, ForeignKey('role.id'))
)


class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False, unique=True)
    _password = db.Column(db.String(128))
    email = db.Column(db.String(144), nullable=False)
    balance = db.Column(db.Integer, nullable=False) 
    _roles = db.relationship("Role", secondary=account_role, backref='accounts')
    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext).decode('utf-8')

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    def __init__(self, name, username, password, email):
        self.name = name
        self.username = username
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.email = email
        self.balance = 0

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @property
    def roles(self):
        return ["ADMIN"]
