from webapp import app
from flask import render_template, url_for, redirect
from webapp.forms import ScanSelfForm, ScanOtherForm, RegisterForm, LoginForm

@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html')

@app.route("/scan", methods=["GET", "POST"])
def scan():
    scan_self_form = ScanSelfForm()
    scan_other_form = ScanOtherForm()
    if scan_self_form.validate_on_submit():
        return redirect(url_for('personal_scan'))
    elif scan_other_form.validate_on_submit():
        return redirect(url_for('report'))
    return render_template('scan.html', title='Scan', scan_self_form=scan_self_form, scan_other_form=scan_other_form)

@app.route("/personal_scan")
def personal_scan():
	return render_template('personal_scan.html', title='Personal Scan')

@app.route("/report")
def report():
	return render_template('report.html', title='Report')

@app.route("/database")
def database():
	return render_template('database.html', title='Database')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('scan'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == '123456@gmail.com' and form.password.data == '123456':
            return redirect(url_for('scan'))
    return render_template('login.html', title='Login', form=form)
