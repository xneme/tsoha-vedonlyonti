from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    name = StringField("Name", [validators.InputRequired()])
    username = StringField("Username", [validators.Length(min=2)])
    email = StringField("Email", [validators.InputRequired(), validators.Email()])
    password = PasswordField("Password", [validators.Length(min=4), validators.EqualTo('confirm', message="Passwords must match.")])
    confirm = PasswordField("Repeat password", [ validators.EqualTo('password', message="Passwords must match.")])

    class Meta:
        csrf = False 
