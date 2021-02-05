from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ScanForm(FlaskForm):

    your_handle = StringField("Enter your handle to scan your followers")
    submit_my_handle = SubmitField("Get Followers")
    user_handle = StringField("or enter a user's handle to see their report")
    submit_other_handle = SubmitField("View Report")