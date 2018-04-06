from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators

class ParticipantForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2)])
    description = StringField("Description")

    class Meta:
        csrf = False


class Comment(FlaskForm):
    text = StringField("Comment", [validators.Length(min=1)])
    like = BooleanField("Interested?")


    class Meta:
        csrf = False


class ContestForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2)])
    description = StringField("Description")


    class Meta:
        csrf = False
        
