from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class ReportForm(FlaskForm):
    username = StringField('Twitter Username Of Account To Be Reported', 
                           validators=[DataRequired(), Length(min=4, max=15)])
    
    threat_field = SelectField('What Bad Thing Did This User Do', 
                               choices=[("Racism", "Racism"),("Homophobia", "Homophobia"), ("Sexism","Sexism"), ("Transphobia","Transphobia"), ("Fraud", "Fraud")], 
                               validators=[DataRequired()])
    
    summary = TextAreaField('Summary Of What Happened (at least 10 characters)', 
                           validators=[DataRequired(), Length(min=10, max=500)])
    
    submit = SubmitField("Report Account")
    
    
class SearchForm(FlaskForm):
    username = StringField('Enter Username To View Reports', 
                           validators=[DataRequired(), Length(min=4, max=15)]) # twitter usernames are between 4 and 15 characters
    submit = SubmitField("Search")
    
    
class ScanForm(FlaskForm):
    username = StringField('', 
                           validators=[DataRequired(), Length(min=4, max=15)])
    submit = SubmitField("Go!")
    

class SliderForm(FlaskForm):
    follower_count = IntegerRangeField('Follower Count', default=0)
    submit = SubmitField('Go')
