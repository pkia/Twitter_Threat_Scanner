from flask import render_template, url_for, flash, redirect, request
from webapp.forms import ReportForm, SearchForm, ScanForm, SliderForm
from webapp.models import Report, User, OAuth
from flask_login import login_user, current_user, logout_user, login_required
from flask_dance.contrib.twitter import twitter
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
from webapp import app
from webapp import db, twitter_blueprint
from sqlalchemy import func, desc
from webapp import api
from datetime import datetime
from webapp import tweepy
import pandas as pd
from webapp import scanning

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', title="Home Page") # Home page


@app.route("/login")
def login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))
    settings = twitter.get('account/settings.json')
    settings_json = settings.json() # convert to dictionary
    return '@{} is logged in to Tweet Guard'.format(settings_json['screen_name'])

@oauth_authorized.connect_via(twitter_blueprint)
def logged_in(blueprint, token):
    settings = blueprint.session.get('account/settings.json')
    if settings.ok:
        settings_json = settings.json()
        username = settings_json['screen_name']
        query = User.query.filter_by(username=username)
        try:
            user = query.one()
        except NoResultFound:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        
@app.route("/logout")
def logout():
    logout_user()
    del twitter_blueprint.token
    return redirect(url_for('index'))


@app.route("/scan", methods=["GET", "POST"])
def scan():
    scan_user_form = ScanForm() # forms for scanning
    if scan_user_form.submit.data and scan_user_form.validate_on_submit(): # if scan "user" form is submitted and validates
        scan_user_form.username.data = scan_user_form.username.data.lower() # put input into lowercase
        try:
            if scanning.check_if_protected(scan_user_form.username.data):
                flash(f"Sorry. That account is protected", "Failure")
            else:
                return redirect(url_for("scan_user", username=scan_user_form.username.data)) # else continue to scan_user page and scan the target
        except:
             flash(f"Sorry. That account does not exist", "Failure") # If it can't find the target account then it doesn't exist and notify user
             
    return render_template('scan.html', scan_user_form=scan_user_form, title="Scan")


@app.route("/scan/user/<string:username>")
def scan_user(username):
    tweets, account_summary, profile = scanning.scan(username) # scan the target
    length = len(tweets)
    return render_template('scan_user.html', tweets=tweets, account_summary=account_summary, profile=profile, length=length, title="Scan A User")


@app.route("/selected_followers", methods=["POST"])
def process_followers():
    form = request.form
    followers = list(form.keys())
    username = followers.pop(0)
    user_profile = scanning.get_twitter_info(username)
    scan_results = scanning.scan_all_function(followers)
    length = len(scan_results)
    return render_template('scan_all.html', user_profile=user_profile, length=length, scan_results=scan_results, title="Scan All")

@app.route("/scan/choose/<string:username>", methods=["GET", "POST"])
@login_required
def scan_choose(username):
    slider_form = SliderForm() # slider for choosing the amount of recent followers to scan in an account
    if slider_form.submit.data: # if user submits slider
        return redirect(url_for("scan_all", username=username, follower_count=slider_form.follower_count.data)) # redirect to scan_all page with x amount of followers to scan
    followers = scanning.get_followers(username) # returns list of followers screen_name's
    follower_profiles_list = []
    user_profile = scanning.get_twitter_info(username)
    for follower in followers:
        follower_profile = scanning.get_twitter_info(follower) # get the twitter profile of all the follower's that there is an option of being scanned
        follower_profiles_list.append(follower_profile) # so that the user can click and select them
    return render_template("scan_choose.html", follower_list=follower_profiles_list, form=slider_form, user_profile=user_profile, title="Choose Followers To Scan")

@app.route("/selected_followers", methods=["POST"])
def process_followers():
    form = request.form.to_dict(flat=True)
    followers = list(form.keys())
    username = followers.pop(0)
    user_profile = scanning.get_twitter_info(username)
    scan_results = scanning.scan_all_function(username, followers)
    length = len(scan_results)
    print(scan_results)
    return render_template('scan_all.html', user_profile=user_profile, length=length, scan_results=scan_results, title="Scan Selected")

    
    
@app.route("/scan/all/<string:username>/<int:follower_count>")
def scan_all(username, follower_count):
    followers = scanning.get_followers(username, follower_count) # get x most recent followers ids for target's account
    scan_results = scanning.scan_all_function(followers) # scan all these followers and save results 
    user_profile = scanning.get_twitter_info(username) # get the user's profile
    length = len(scan_results) # get the length of the scan results (to iterate through list on the html page)
    print(scan_results)
    return render_template('scan_all.html', user_profile=user_profile, length=length, scan_results=scan_results, title="Scan All")


@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    form = ReportForm() # form to report an account
    if form.validate_on_submit(): # if form val on submit
        form.username.data = form.username.data.lower() # turn input to lowercase
        try:
            scanning.get_twitter_info(form.username.data) # check if account exists
            report = Report(account_id=form.username.data, threat_type=form.threat_field.data, summary=form.summary.data) # make report for account if it does
            db.session.add(report) # then add report
            db.session.commit() # commit changes
            flash(f"Report Submitted For @{form.username.data}!", "Success") # show a flash message that the operation was a success
            return redirect(url_for("database"))
        except:
            flash(f"Sorry. That account does not exist", "Failure") # if account doesn't exist then flash this
    return render_template('report.html', form=form, title="Make A Report")


@app.route("/database", methods=["GET", "POST"])
def database():
    form = SearchForm()
    if form.validate_on_submit():
        form.username.data = form.username.data.lower()
        try:
            scanning.get_twitter_info(form.username.data) # if the user exists then report them
            return redirect(url_for("database_search", username=form.username.data, page=1))
        except:
            flash(f"Sorry. That account does not exist", "Failure")
        
    page = request.args.get("page", 1, type=int)
    reports = Report.query.order_by(Report.date_submitted.desc()).paginate(per_page=5) # fetch a paginated list of recent reports in order of date submitted desc
    return render_template('database.html', form=form, reports=reports, title="Database")


@app.route("/database/<string:username>")
def database_search(username):
    page = request.args.get("page", 1, type=int)
    if Report.query.filter_by(account_id=username).first() != None:
        reports = Report.query.filter_by(account_id=username).order_by(Report.date_submitted.desc()).paginate(per_page=5)
    else:
    	reports = None
    user_profile = scanning.get_twitter_info(username)
    return render_template('database_search.html', reports=reports, user_profile=user_profile, title="Database Search")

@app.route("/database/report_ranked")
def report_ranked():
    page = request.args.get("page", 1, type=int)
    count = db.session.query(Report.account_id, func.count(Report.account_id).label(
        "total")).group_by(Report.account_id) # this gets the total reports grouped by account, ordered by total reports
    count = count.order_by(desc('total')) # it is a list of tuples (screen_name, count)
    counts2 = count.paginate(per_page=5) # this variable is just a paginated version of count^
    user_profiles = []
    for tup in count: # for tuple in count variable
        user_profile= scanning.get_twitter_info(tup[0]) # get the twitter profile of the screen_name
        user_profiles.append(user_profile) # add it to a list
    length = len(user_profiles)
    return render_template('report_ranked.html', count=count, counts2=counts2, user_profiles=user_profiles, length=length, title="Reports Ranked")

@app.route('/unfollow_user/<string:screen_name>', methods = ['GET', 'POST'])
def unfollow_user(screen_name):
    if request.method == 'POST':
        scanning.unfollow_user(screen_name)
        return 'User Unfolllowed!'
