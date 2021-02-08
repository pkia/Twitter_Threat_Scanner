from flask import render_template, url_for, flash, redirect, request
from webapp.forms import ReportForm, SearchForm, ScanForm1, ScanForm2, ScanSelfForm, ScanOtherForm, LoginForm, RegisterForm
from webapp.models import Account, Report, ScanResult
from webapp import app
from webapp import db
from sqlalchemy import func, desc
from webapp import api
from datetime import datetime, timedelta
from webapp import tweepy
import random


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')
  
@app.route("/scan1", methods=["GET", "POST"])
def scan1():
    scan_self_form = ScanSelfForm()
    scan_other_form = ScanOtherForm()
    if scan_self_form.validate_on_submit():
        return redirect(url_for('personal_scan'))
    elif scan_other_form.validate_on_submit():
        return redirect(url_for('report'))
    return render_template('scan.html', title='Scan', scan_self_form=scan_self_form, scan_other_form=scan_other_form)
  
  
@app.route("/scan", methods=["GET", "POST"])
def scan():
    
    scan_all_form = ScanForm1()
    scan_user_form = ScanForm2()
    if scan_user_form.submit2.data and scan_user_form.validate_on_submit():
        try:
            acc = api.get_user(scan_user_form.username.data)
            if acc.protected:
                flash(f"Sorry. That account is protected", "Failure")
            else:
                return redirect(url_for("scan_user", username=scan_user_form.username.data))
        except:
             flash(f"Sorry. That account does not exist", "Failure")

    if scan_all_form.submit1.data and scan_all_form.validate_on_submit():
        try:
            acc = api.get_user(scan_user_form.username.data)
            if acc.protected:
                flash(f"Sorry. That account is protected", "Failure")
            else:
                return redirect(url_for("scan_all", username=scan_all_form.username.data))
        except:
             flash(f"Sorry. That account does not exist", "Failure")
             
    return render_template('scan.html', scan_all_form=scan_all_form, scan_user_form=scan_user_form, title="Scan")


@app.route("/scan/user/<string:username>")
def scan_user(username):
    result = scan_user_function(username)
    user_profile = get_twitter_info(username)
    
    if result != None:
        account = Account.query.filter_by(id=username).first()
    else:
        account = None
    return render_template('scan_user.html', result=result, user_profile=user_profile, account=account, title="Scan A User")

# make scan_all_function return an account rather than a username so i can include reports

@app.route("/scan/all/<string:username>")
def scan_all(username):
    
    results = scan_all_function(username)
    user_profile = get_twitter_info(username)
    bad_user_profiles=[]
    length = len(results)
    if length > 0:
        for result in results:
            profile = get_twitter_info(result[0])
            bad_user_profiles.append(profile)
    return render_template('scan_all.html', user_profile=user_profile, bad_user_profiles=bad_user_profiles, length=length, results=results, title="Scan All")


@app.route("/report", methods=["GET", "POST"])
def report():
    form = ReportForm()
    if form.validate_on_submit():
        try:
            api.get_user(form.username.data)
            report = Report(account_id=form.username.data, threat_type=form.threat_field.data, summary=form.summary.data)
            if Account.query.filter_by(id=form.username.data).first() == None:
                account = Account(id=form.username.data)
                db.session.add(account)
            db.session.add(report)
            db.session.commit()
            flash(f"Report Submitted For @{form.username.data}!", "Success")
            return redirect(url_for("database"))
        except:
            flash(f"Sorry. That account does not exist", "Failure")
    return render_template('report.html', form=form, title="Make A Report")


@app.route("/database", methods=["GET", "POST"])
def database():
    form = SearchForm()
    if form.validate_on_submit():
        try:
            api.get_user(form.username.data)
            return redirect(url_for("database_search", username=form.username.data, page=1))
        except:
            flash(f"Sorry. That account does not exist", "Failure")
        
    page = request.args.get("page", 1, type=int)
    reports = Report.query.order_by(Report.date_submitted.desc()).paginate(per_page=5)
    return render_template('database.html', form=form, reports=reports, title="Database")


@app.route("/database/<string:username>")
def database_search(username):
    page = request.args.get("page", 1, type=int)
    scan_results = ScanResult.query.filter_by(account_id=username).first()
    print(scan_results)
    if Report.query.filter_by(account_id=username).first() != None:
        reports = Report.query.filter_by(account_id=username).order_by(Report.date_submitted.desc()).paginate(per_page=5)
    else:
    	reports = None
    user_profile = get_twitter_info(username)
    return render_template('database_search.html', reports=reports, scan_results=scan_results, user_profile=user_profile, title="Database Search")


@app.route("/database/report_ranked")
def report_ranked():
    page = request.args.get("page", 1, type=int)
    count = db.session.query(Report.account_id, func.count(Report.account_id).label(
        "total")).group_by(Report.account_id)
    count = count.order_by(desc('total'))
    counts2 = count.paginate(per_page=5)
    user_profiles = []
    for tup in count:
        user_profile= get_twitter_info(tup[0])
        user_profiles.append(user_profile)
    length = len(user_profiles)
    return render_template('report_ranked.html', count=count, counts2=counts2, user_profiles=user_profiles, length=length, title="Reports Ranked")

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


def scan(username):
    ScanResult.query.filter_by(account_id=username).delete()
    db.session.commit()
    ran = random.randint(0,5)
    if ran <= 2:
        return None
    if Account.query.filter_by(id=username).first() == None:
        account = Account(id=username)
        db.session.add(account)
    result = ScanResult(threat_detected="racist", threat_level=9, account_id=username)
    db.session.add(result)
    db.session.commit()
    scan_results = ScanResult.query.filter_by(account_id=username).first()
    return result

def scan_user_function(username): 
    scan_result = scan(username)
    return scan_result
    
def scan_all_function(username):
    followers = get_followers(username) # get all a user's followers
    bad = [] # list of usernames where something bad was found
    for follower in followers:
        if get_twitter_info(follower) == False: # make this a standalone get_if_priv() func
        	print("private")
        	continue
        scan_result = scan_user_function(follower) # get scan_results of every follower
        if scan_result != None:
            results = [follower, scan_result, Account.query.filter_by(id=follower)] # 
            bad.append(results)
    return bad

def get_twitter_info(screen_name):
    user_info = api.get_user(screen_name)
    if user_info.protected == True:
    	return False
    profile = [user_info.screen_name, user_info.name, user_info.profile_image_url]
    return profile

def get_followers(screenname, limit=50):
    follower_list = []
    if limit < 0:
        raise Exception("Enter a number above 0!")
    elif limit > 50:  # Basic error control
        raise Exception("Max limit 50")
    for follower in tweepy.Cursor(api.followers, screenname).items(int(limit)):  # Uses tweepys cursor function to add most recent followers to a list
        follower_list.append(follower.screen_name)
    return follower_list