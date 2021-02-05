from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length


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
    
