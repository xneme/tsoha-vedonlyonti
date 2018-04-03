# flask-sovellus
from flask import Flask
app = Flask(__name__)

# tietokanta
from flask_sqlalchemy import SQLAlchemy
import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

# salasanojen kryptaus
from flask_bcrypt import Bcrypt
app.config["BCRYPT_LOG_ROUNDS"] = 12

bcrypt = Bcrypt(app)

# sovelluksen toiminnallisuudet
from application import views

from application.tasks import models
from application.tasks import views

from application.auth import models
from application.auth import views

# kirjautuminen
from application.auth.models import User
from os import urandom

app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# luodaan tietokantataulut tarvittaessa
try:
    db.create_all()
except:
    pass
