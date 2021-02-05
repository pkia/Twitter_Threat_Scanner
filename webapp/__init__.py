from flask import Flask


app = Flask(__name__)
#import secrets
#secrets.token_hex(16)
app.config['SECRET_KEY'] = '3efb586753c505b1b6dc3672351a27cf'


from webapp import views