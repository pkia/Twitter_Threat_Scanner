from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class ReportForm(FlaskForm):
    username = StringField('Twitter Username Of Account To Be Reported', 
                           validators=[DataRequired(), Length(min=4, max=15)])
    
    threat_field = SelectField('What Bad Thing Did This User Do', 
                               choices=[("racism", "racism"),("prick", "Being a Prick")],
                               validators=[DataRequired()])
    
    summary = TextAreaField('Summary Of What Happened (at least 10 characters)', 
                           validators=[DataRequired(), Length(min=10, max=500)])
    
    submit = SubmitField("Report Account")
    
    
class SearchForm(FlaskForm):
    username = StringField('Twitter Username Of Account To Search For', 
                           validators=[DataRequired(), Length(min=4, max=15)])
    submit = SubmitField("Search For Reports On Account")
    
    
class ScanForm1(FlaskForm):
    username = StringField('', 
                           validators=[DataRequired(), Length(min=4, max=15)])
    submit1 = SubmitField("Go!")
    
    
class ScanForm2(FlaskForm):
    username = StringField('', 
                           validators=[DataRequired(), Length(min=4, max=15)])
    submit2 = SubmitField("Go!")
    

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
