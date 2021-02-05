from webapp import app
from flask import render_template, url_for, redirect, flash
from webapp.forms import ScanForm

@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html')

@app.route("/scan", methods=["GET", "POST"])
def scan():
	form = ScanForm()
	if form.your_handle.data and form.user_handle.data:
		flash("Only one field required", "danger")
	elif form.your_handle.data:
		return redirect(url_for('personal_scan'))
	elif form.submit_other_handle.data:
		return redirect(url_for('report'))
	return render_template('scan.html', title='Scan', form=form)

@app.route("/personal_scan")
def personal_scan():
	return render_template('personal_scan.html', title='Personal Scan')

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
