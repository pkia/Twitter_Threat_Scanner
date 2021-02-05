from flask import render_template, url_for, flash, redirect, request
from webapp.form import ReportForm, SearchForm, ScanForm1, ScanForm2
from webapp.models import Account, Report, ScanResult
from webapp import app
from webapp import db
from sqlalchemy import func
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
        try:
            api.get_user(scan_user_form.username.data)
            return redirect(url_for("scan_user", username=scan_user_form.username.data))
        except:
             flash(f"Sorry. That account does not exist", "Failure")

    if scan_all_form.submit1.data and scan_all_form.validate_on_submit():
        try:
            api.get_user(scan_all_form.username.data)
            return redirect(url_for("scan_all", username=scan_all_form.username.data))
        except:
             flash(f"Sorry. That account does not exist", "Failure")
             
    return render_template('scan_home.html', scan_all_form=scan_all_form, scan_user_form=scan_user_form, title="Scan Home")


@app.route("/scan/user/<string:username>")
def scan_user(username):
    
    result = scan_user_function(username)
    user_profile = get_twitter_info(username)
    if result != None:
        account = Account.query.filter_by(id=username).first()
        clearScan = False
    else:
        account = None
        clearScan = True
    return render_template('scan_user.html', result=result, user_profile=user_profile, account=account, clearScan=clearScan, title="Scan User")

# make scan_all_function return an account rather than a username so i can include reports

@app.route("/scan/all/<string:username>")
def scan_all(username):
    
    results = scan_all_function(username)
    user_profile = get_twitter_info(username)
    bad_user_profiles=[]
    clearScan = False
    length = len(results)
    if length > 0:
        for result in results:
            profile = get_twitter_info(result[0])
            bad_user_profiles.append(profile)
    else:
        clearScan=True
    return render_template('scan_all.html', user_profile=user_profile, bad_user_profiles=bad_user_profiles, length=length, results=results, clearScan=clearScan, title="Scan All")


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
    account = Account.query.filter_by(id=username).first()
    try:
        reports = Report.query.filter_by(account_holder=account).order_by(Report.date_submitted.desc()).paginate(per_page=5)
    except:
        reports = None
    user_profile = get_twitter_info(username)
    return render_template('database_search.html', reports=reports, account=account, user_profile=user_profile, title="Database Search")


@app.route("/database/report_ranked")
def report_ranked():
    page = request.args.get("page", 1, type=int)
    count = db.session.query(Report.account_id, func.count(Report.account_id).label(
        "total")).group_by(Report.account_id).order_by("total")
    counts2 = count.paginate(per_page=5)
    user_profiles = []
    for tup in count:
        user_profile= get_twitter_info(tup[0])
        user_profiles.append(user_profile)
    length = len(user_profiles)
    return render_template('report_ranked.html', count=count, counts2=counts2, user_profiles=user_profiles, length=length, title="Reports Ranked")

@app.route("/register")
def register():
	return render_template('register.html', title='Register')

@app.route("/login")
def login():
	return render_template('login.html', title='Login')



def scan(username):
    if random.randint(0,2) == 1 or 2:
        result = None
        return result
    result = ScanResult(threat_detected="racist", threat_level=9, account_id=username)
    account = Account(id=username)
    db.session.add(result)
    db.session.add(account)
    db.session.commit()
    return result

#TODO: implement something that deletes old scan results if new one given


def scan_user_function(username, redo=False):
    account = Account.query.filter_by(id=username).first() # searches for account
    if account != None: 
        scan_result = ScanResult.query.filter_by(account_id=username).first() # if present and scanned less than two weeks ago, return that scan
        if scan_result != None:
            date = scan_result.date_scanned
            date_two_weeks_ago = date - timedelta(days=14)
        
            if date > date_two_weeks_ago:
                if redo:
                    scan_result = scan(username)
            else:
                scan_result = scan(username)
        else: # if not scanned ever
                scan_result = scan(username) # evan's side of stuff
            
    else:
        scan_result = scan(username)
    return scan_result
    
def scan_all_function(username):
    followers = get_followers(username) # get all a user's followers
    bad = [] # list of usernames where something bad was found
    for follower in followers:
        scan_result = scan_user_function(follower) # get scan_results of every follower
        if scan_result != None:
            results = [follower, scan_result, Account.query.filter_by(id=follower)] # 
            bad.append(results)
    return bad

def get_twitter_info(screen_name):
    user_info = api.get_user(screen_name)
    profile = [user_info.screen_name, user_info.name, user_info.profile_image_url]
    return profile

def get_followers(username):
    followersList = []
    for follower in api.followers(username, include_user_entities=False):
        followersList.append(follower.screen_name)
    return followersList
