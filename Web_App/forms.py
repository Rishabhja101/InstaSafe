from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField("Login")

class InstasafeForm(FlaskForm):
    username_list = StringField("Enter a list of usernames each seperated by a comma", validators=[DataRequired()])

    submit = SubmitField("Submit")
