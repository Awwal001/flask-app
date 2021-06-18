from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField

class Addform(FlaskForm):

    name = StringField('Name of Puppy: ')
    submit = SubmitField('Add Puppy')

class Delform(FlaskForm):

    id = IntegerField("Id Number of Puppy to remove: ")
    submit = SubmitField("Remove Puppy")


class AddOwner(FlaskForm):

    name = StringField('Name of owner: ')
    id = IntegerField("Id Number of Puppy you'd like to adopt: ")
    submit = SubmitField("Adopt...")