from webapp import app
from flask import render_template

@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html')

@app.route("/scan")
def scan():
	return render_template('scan.html', title='Scan')

@app.route("/report")
def report():
	return render_template('report.html', title='Report')

@app.route("/database")
def database():
	return render_template('database.html', title='Database')

@app.route("/register")
def register():
	return render_template('register.html', title='Register')

@app.route("/login")
def login():
	return render_template('login.html', title='Login')
