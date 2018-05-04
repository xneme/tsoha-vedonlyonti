from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, SelectField, RadioField, TextAreaField, validators
from wtforms.fields.html5 import DateField


class BetForm(FlaskForm):
    amount = IntegerField("Amount")
    participant = SelectField("Who is going to win?", coerce=int)


    class Meta:
        csrf = False


class CommentForm(FlaskForm):
    text = StringField("Comment", [validators.Length(min=1)])
    like = BooleanField("Interested?")


    class Meta:
        csrf = False


class EventForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2)])
    description = TextAreaField("Description")
    date_start = DateField("Betting starts", format="%Y-%m-%d")
    date_end = DateField("Betting ends", format="%Y-%m-%d")


    class Meta:
        csrf = False


class ParticipantForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2)])
    description = TextAreaField("Description")


    class Meta:
        csrf = False


class EventParticipantForm(FlaskForm):
    participant_id = SelectField("Participant", coerce=int)


    class Meta:
        csrf = False
        
