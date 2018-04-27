from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField, RadioField, TextAreaField, validators


class BetForm(FlaskForm):
    amount = StringField("Name", [validators.Length(min=2)])
    guess = RadioField("Quess:", choices=[('with', 'betting with'),('against', 'betting against')])


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
        
