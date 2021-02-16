from flask import render_template, url_for, flash, redirect, request
from webapp.forms import ReportForm, SearchForm, ScanForm1, ScanForm2, SliderForm
from webapp.models import Account, Report, ScanResult, User, OAuth
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
import random
import pandas as pd
from joblib import load


@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html', title="Home Page")


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
    username = username.lower()
    scan_user_function(username)
    user_profile = get_twitter_info(username)
    scan_result = ScanResult.query.filter_by(account_id=username).all()
    return render_template('scan_user.html', user_profile=user_profile, scan_result=scan_result, title="Scan A User")


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
    length = len(results)
    return render_template('scan_all.html', user_profile=user_profile, followers=followers, length=length, results=results, title="Scan All")


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


def scan(username):
    ScanResult.query.filter_by(account_id=username).delete()
    db.session.commit()
    tweets = tweetpull(username)
    pipeline = load("webapp/LogisticRegression/text_class1.joblib")
    
    tweets['prediction'] = pipeline.predict(tweets['tweet_text'])
    data = tweets.prediction.value_counts()
    bad_tweets = tweets.loc[tweets['prediction'] == 1]
    results = [bad_tweets["tweet_id"], bad_tweets["tweet_text"], data]
    return results

def scan_user_function(username): 
    username = username.lower()
    results = scan(username)
    print(results)
    scan_results = []
    if len(results[0]) > 0:
        if Account.query.filter_by(id=username).first() == None:
            account = Account(id=username)
            db.session.add(account)
            db.session.commit()
        for item in results[0].iteritems():
            scan_result = ScanResult(id=item[1], threat_detected="hatespeech", account_id=username)
            db.session.add(scan_result)
            scan_results.append(scan_result)
        db.session.commit()
    return scan_results
    
def scan_all_function(username, followers):
    bad = [] # list of usernames where something bad was found
    for follower in followers:
        profile = get_twitter_info(follower)
        for thing in profile:
            print(thing)
        if profile[3] == True:
        	print("private user")
        	continue
        scan_results = scan_user_function(follower) # get scan_results of every follower
        if len(scan_results) > 0:
            results = [profile, scan_results] # 
            bad.append(results)
    return bad

def get_twitter_info(screen_name):
    screen_name = screen_name.lower()
    user_info = api.get_user(screen_name)
    profile = [user_info.screen_name.lower(), user_info.name, user_info.profile_image_url, user_info.protected]
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


def tweetpull(screen_name):
    profile = get_twitter_info(screen_name)
    alltweets = []  # List to buffer incoming tweets before being formatted for pd.dict
    if profile[3] is False: # if not protected acc
        new_tweets = api.user_timeline(screen_name=screen_name, count=200)  # Limitation to amount of tweets able to pull by twitter api
        alltweets.extend(new_tweets)  # Saving most recent tweets to alltweets
        if len(alltweets) > 0:
            oldest = alltweets[-1].id - 1  # Acts as counter for the each iteration starting at the oldest possible tweet -1
        while len(new_tweets) > 0:
            new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1  # Asks almost like a pointer that allows the func to see which tweet it needs to pull next

    outtweets = [{'created_at': tweet.created_at,  # Makes new formatted list of tweets using a pandas dict format to allow further data manipulation in future functions
                  'tweet_id': tweet.id,
                  'tweet_text': tweet.text} for tweet in alltweets]
    return pd.DataFrame.from_dict(outtweets)

    
