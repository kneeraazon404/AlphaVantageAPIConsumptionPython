from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, validators
from wtforms.validators import InputRequired, ValidationError

class RegForm(FlaskForm):
    username = StringField(label='Username', validators=[InputRequired()])
    fname = StringField(label='First name', validators=[InputRequired()])
    lname = StringField(label='Last name', validators=[InputRequired()])
    email = EmailField(label='E-mail address', validators=[InputRequired()])
    password = PasswordField(label='Password', validators=[InputRequired()])
    # confpword = PasswordField(label='Confirm your password', validators=[InputRequired()])
    submit = SubmitField('Submit')