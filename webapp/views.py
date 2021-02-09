from flask import render_template, url_for, flash, redirect, request
from webapp.forms import ReportForm, SearchForm, ScanForm1, ScanForm2, LoginForm, RegisterForm, SliderForm
from webapp.models import Account, Report, ScanResult
from webapp import app
from webapp import db
from sqlalchemy import func, desc
from webapp import api
from datetime import datetime, timedelta
from webapp import tweepy
import random

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', title="Home Page")

@app.route("/scan", methods=["GET", "POST"])
def scan():
    
    scan_all_form = ScanForm1()
    scan_user_form = ScanForm2()
    if scan_user_form.submit2.data and scan_user_form.validate_on_submit():
        scan_user_form.username.data = scan_user_form.username.data.lower()
        try:
            acc = api.get_user(scan_user_form.username.data)
            if acc.protected:
                flash(f"Sorry. That account is protected", "Failure")
            else:
                return redirect(url_for("scan_user", username=scan_user_form.username.data))
        except:
             flash(f"Sorry. That account does not exist", "Failure")

    if scan_all_form.submit1.data and scan_all_form.validate_on_submit():
        scan_all_form.username.data = scan_all_form.username.data.lower()
        try:
            acc = api.get_user(scan_all_form.username.data)
            if acc.protected:
                flash(f"Sorry. That account is protected", "Failure")
            else:
                return redirect(url_for("scan_choose", username=scan_all_form.username.data))
        except:
             flash(f"Sorry. That account does not exist", "Failure")
             
    return render_template('scan.html', scan_all_form=scan_all_form, scan_user_form=scan_user_form, title="Scan")


@app.route("/scan/user/<string:username>")
def scan_user(username):
    result = scan_user_function(username)
    user_profile = get_twitter_info(username)
    return render_template('scan_user.html', result=result, user_profile=user_profile, title="Scan A User")


@app.route("/scan/choose/<string:username>", methods=["GET", "POST"])
def scan_choose(username):
    slider_form = SliderForm()
    if slider_form.submit.data:
        print(slider_form.follower_count.data)
        return redirect(url_for("scan_all", username=username, follower_count=slider_form.follower_count.data))
    followers = get_followers(username)
    follower_list = []
    for follower in followers:
        follower_profile = get_twitter_info(follower)
        follower_list.append(follower_profile)
    return render_template("scan_choose.html", follower_list=follower_list, form=slider_form, title="Choose Followers To Scan")
    
    
@app.route("/scan/all/<string:username>/<int:follower_count>")
def scan_all(username, follower_count):
    followers = get_followers(username, follower_count)
    results = scan_all_function(username, followers)
    user_profile = get_twitter_info(username)
    bad_user_profiles=[]
    length = len(results)
    if length > 0:
        for result in results:
            profile = get_twitter_info(result[0])
            bad_user_profiles.append(profile)
    return render_template('scan_all.html', user_profile=user_profile, bad_user_profiles=bad_user_profiles, followers=followers, length=length, results=results, title="Scan All")


@app.route("/report", methods=["GET", "POST"])
def report():
    form = ReportForm()
    if form.validate_on_submit():
        form.username.data = form.username.data.lower()
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
        form.username.data = form.username.data.lower()
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
    return result

def scan_user_function(username): 
    scan_result = scan(username)
    return scan_result
    
def scan_all_function(username, followers):
    bad = [] # list of usernames where something bad was found
    for follower in followers:
        profile = get_twitter_info(username)
        if profile[3] == True:
        	print("private")
        	continue
        scan_result = scan_user_function(follower) # get scan_results of every follower
        if scan_result != None:
            results = [follower, scan_result] # 
            bad.append(results)
    return bad

def get_twitter_info(screen_name):
    user_info = api.get_user(screen_name)
    profile = [user_info.screen_name, user_info.name, user_info.profile_image_url, user_info.protected]
    return profile

def get_followers(screenname, limit=10):
    follower_list = []
    if limit < 0:
        raise Exception("Enter a number above 0!")
    elif limit > 100:  # Basic error control
        raise Exception("Max limit 100")
    for follower in tweepy.Cursor(api.followers, screenname).items(int(limit)):  # Uses tweepys cursor function to add most recent followers to a list
        follower_list.append(follower.screen_name)
    return follower_list
