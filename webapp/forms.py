from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class ScanSelfForm(FlaskForm):

    handle = StringField("Enter your handle to scan your followers", validators=[DataRequired()])
    submit = SubmitField("Get Followers")

class ScanOtherForm(FlaskForm):

    handle = StringField("or enter a user's handle to see their report", validators=[DataRequired()])
    submit = SubmitField("View Report")

class RegisterForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=1, max=15)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
	retype_password = PasswordField('Retype Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')