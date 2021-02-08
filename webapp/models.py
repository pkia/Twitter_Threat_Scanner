from datetime import datetime
from webapp import db

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
    threat_level = db.Column(db.Integer)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    
    def __repr__(self):
        return f"ScanResult('{self.id}', '{self.threat_detected}', '{self.date_scanned}', '{self.threat_level}')"
