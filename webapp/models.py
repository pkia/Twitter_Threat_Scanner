from datetime import datetime
from webapp import db, twitter_blueprint, login_manager
from flask_login import UserMixin, current_user
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

twitter_blueprint.backend = SQLAlchemyStorage(OAuth, db.session, user=current_user)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threat_type = db.Column(db.String(50), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    
    def __repr__(self):
        return f"Report('{self.id}', '{self.threat_type}', '{self.summary}', '{self.date_submitted}')"
    
    
class Account(db.Model):
    id = db.Column(db.String(15), primary_key=True)
    report = db.relationship('Report', backref="account_holder", lazy=True)
    scan_results = db.relationship('ScanResult', backref="account_holder", lazy=True)
                              
    def __repr__(self):
        return f"Account('{self.id}', '{self.report}', '{self.scan_results}')"
    
    
class ScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threat_detected = db.Column(db.String(50), nullable=False)
    date_scanned = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    
    def __repr__(self):
        return f"ScanResult('{self.id}', '{self.threat_detected}', '{self.date_scanned}')"
