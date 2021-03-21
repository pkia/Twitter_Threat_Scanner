from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from markupsafe import Markup



class ReportForm(FlaskForm):
    username = StringField('Account Name', 
                           validators=[DataRequired(), Length(min=3, max=15)])
    
    threat_field = SelectField('Threat Type',
                               choices=["Racism", "Hate", "Violence", "Sexism", "Homophobia", "Transphobia", "Offensive", "Fraud"], 
                               validators=[DataRequired()])
    
    summary = TextAreaField("Report Summary" + Markup('<br>') + Markup('<small>') + "(at least 10 characters)" + Markup('</small>'), 
                           validators=[DataRequired(), Length(min=10, max=500)])
    
    submit = SubmitField("Report Account")
    
    
class SearchForm(FlaskForm):
    username = StringField('Search username to View Reports', 
                           validators=[DataRequired(), Length(min=3, max=15)]) # twitter usernames are between 4 and 15 characters
    submit = SubmitField(Markup('&#x276F;'))
    
    
class ScanForm(FlaskForm):
    username = StringField("Enter another user's handle to scan", 
                           validators=[DataRequired(), Length(min=3, max=15)])
    submit = SubmitField(Markup('&#x276F;'))
    

class SliderForm(FlaskForm):
    follower_count = IntegerRangeField('Follower Count', default=0)
    submit = SubmitField('Go')
