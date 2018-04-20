from sqlalchemy.ext.hybrid import hybrid_property
from application import bcrypt, db
from application.models import Base
from sqlalchemy.sql import text

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False, unique=True)
    _password = db.Column(db.String(128))
    email = db.Column(db.String(144), nullable=False)
    
    tasks = db.relationship("Task", backref='account', lazy=True)

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
