from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ScanSelfForm(FlaskForm):

    handle = StringField("Enter your handle to scan your followers", validators=[DataRequired()])
    submit = SubmitField("Get Followers")

class ScanOtherForm(FlaskForm):

    handle = StringField("or enter a user's handle to see their report", validators=[DataRequired()])
    submit = SubmitField("View Report")