from datetime import datetime
from webapp import db, twitter_blueprint, login_manager, app
from flask_login import UserMixin, current_user
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

# returns user object of user_id to login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)
    reports = db.relationship('Report', backref='author', lazy=True)
    # adds important relationship to Report class

# used by twitter blueprint to store user info
class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

twitter_blueprint.backend = SQLAlchemyStorage(OAuth, db.session, user=current_user)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threat_type = db.Column(db.String(50), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # account to be reported
    account_id = db.Column(db.String(15), nullable=False)
    # author of report
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Report('{self.id}', '{self.threat_type}', '{self.summary}', '{self.date_submitted}')"

# restricted index view on admin system
class MyAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.username == "tweetguardxxx"

# restricted database of reports view on admin system
class ReportsView(ModelView):
    def is_accessible(self):
        return current_user.username == "tweetguardxxx"
        
# add views to admin console
admin = Admin(app, index_view=MyAdminView(), template_mode="bootstrap4")
admin.add_view(ReportsView(Report, db.session))