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
from webapp import auth, api
from datetime import datetime
from webapp import tweepy
from webapp import scanning
import pandas as pd
import json
import tweepy


@app.route("/")
@app.route("/index")
def index():
    if twitter.authorized and auth.access_token is None:
        access_key = twitter_blueprint.token['oauth_token']
        access_secret = twitter_blueprint.token['oauth_token_secret']
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
    return render_template('index.html', title="Home Page")  # Home page


@app.route("/login")
def login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))
    settings = twitter.get('account/settings.json')
    settings_json = settings.json()  # convert to dictionary
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
    scan_user_form = ScanForm()  # forms for scanning
    # if scan "user" form is submitted and validates
    if scan_user_form.submit.data and scan_user_form.validate_on_submit():
        # put input into lowercase
        scan_user_form.username.data = scan_user_form.username.data.lower()
        try:
            if scanning.check_if_protected(scan_user_form.username.data): # if account protected
                flash(f"Sorry. That account is protected", "danger")
            else:
                # else continue to scan_user page and scan the target
                return redirect(url_for("scan_user", username=scan_user_form.username.data)) 
        except:
            # If it can't find the target account then it doesn't exist and notify user
            flash(f"Sorry. That account does not exist", "danger")

    return render_template('scan.html', scan_user_form=scan_user_form, title="Scan")


@app.route("/scan/user/<string:username>")
def scan_user(username):
    tweets_json = {}
    tweets, account_summary, profile = scanning.scan(
        username)  # scan the target
    tweets_split = list(divide_tweets(tweets, 10))
    for tweet_array in tweets_split:
        remove_ids(tweet_array)
    for i in range(len(tweets_split)):
        tweet_and_length = {
            'array': tweets_split[i],
            'length': len(tweets_split[i])
        }
        tweets_json[f"tweet-{i}"] = tweet_and_length
    length = len(tweets)
    return render_template('scan_user.html', tweets=tweets_json, length=length, account_summary=account_summary, profile=profile, title="Scan A User")

# Generator function to divide all tweets found into groups of 10 so they're ready for pagination


def divide_tweets(tweets, n):
    for i in range(0, len(tweets), n):
        yield tweets[i:i + n]

# Utility method for changing tweet ids to strings.
# Necessary because flask can't pass long numbers in a template.


def remove_ids(tweet_array):
    for tweet in tweet_array:
        tweet[0] = str(tweet[0])
    return tweet_array


@app.route("/selected_followers", methods=["POST"])
def process_followers():
    form = request.form
    # Creates a list with the usernames of the users selected
    followers = list(form.keys())
    # Logged in username, which is sent in the form as a hidden field
    username = followers.pop(0)
    user_profile = scanning.get_twitter_info(username)
    scan_results = scanning.scan_all_function(followers)
    length = len(scan_results)
    return render_template('scan_all.html', user_profile=user_profile, length=length, scan_results=scan_results, title="Scan All")


@app.route("/scan/choose/<string:username>", methods=["GET", "POST"])
@login_required
def scan_choose(username):
    # slider for choosing the amount of recent followers to scan in an account
    slider_form = SliderForm()
    if slider_form.submit.data:  # if user submits slider
        # redirect to scan_all page with x amount of followers to scan
        return redirect(url_for("scan_all", username=username, follower_count=slider_form.follower_count.data))
    # returns list of followers screen_name's
    followers = scanning.get_followers(username) 
    follower_profiles = []
    user_profile = scanning.get_twitter_info(username) # fetch the info of the person making the scan
    for i in range(len(followers)):
        # get the twitter profile of all the follower's that there is an option of being scanned
        follower_profile = scanning.get_twitter_info(followers[i])
        # so that the user can click and select them
        follower_profiles.append(follower_profile)
    return render_template("scan_choose.html", follower_list=follower_profiles, form=slider_form, user_profile=user_profile, title="Choose Followers To Scan")


@app.route("/scan/all/<string:username>/<int:follower_count>")
def scan_all(username, follower_count):
    # get x most recent followers ids for target's account
    followers = scanning.get_followers(username, follower_count)
    # scan all these followers and save results
    scan_results = scanning.scan_all_function(followers)
    user_profile = scanning.get_twitter_info(
        username)  # get the user's profile
    # get the length of the scan results (to iterate through list on the html page)
    length = len(scan_results)
    return render_template('scan_all.html', user_profile=user_profile, length=length, scan_results=scan_results, title="Scan All")


@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    form = ReportForm()  # form to report an account
    if form.validate_on_submit():  # if form val on submit
        form.username.data = form.username.data.lower()  # turn input to lowercase
        if form.username.data[0] == "@": # if username was entered with an @ at the start
            form.username.data = form.username.data[1:] # remove it
        try:
            # check if account exists
            scanning.get_twitter_info(form.username.data)
            report = Report(account_id=form.username.data, threat_type=form.threat_field.data,
                            summary=form.summary.data, author=current_user)  # make report for account if it does
            db.session.add(report)  # then add report
            db.session.commit()  # commit changes
            # show a flash message that the operation was a success
            flash(f"Report Submitted For @{form.username.data}!", "success")
            return redirect(url_for("database"))
        except:
            # if account doesn't exist then flash this
            flash(f"Sorry. That account does not exist", "danger")
    elif form.summary.data is not None:
        if len(form.summary.data) < 10:
            flash(f"Summary must contain a minimum of 10 characters", "danger")
        else:
            flash(f"Sorry. That username is invalid.", "danger") # if username is invalid then flash this
    return render_template('report.html', form=form, title="Make A Report")


@app.route("/database", methods=["GET", "POST"])
def database():
    form = SearchForm()
    if form.validate_on_submit(): # if validates on sub then put it in lowercase and take the "@" sign if there is one
        form.username.data = form.username.data.lower()
        if form.username.data[0] == "@":
            form.username.data = form.username.data[1:]
        try:
            # if the user exists then report them
            scanning.get_twitter_info(form.username.data)
            return redirect(url_for("database_search", username=form.username.data, page=1))
        except:
            flash(f"Sorry. That account does not exist", "danger")
    elif form.submit.data:
        flash(f"Sorry. That username is invalid.", "danger")
    page = request.args.get("page", 1, type=int)
    # fetch a paginated list of recent reports in order of date submitted desc
    reports = Report.query.order_by(
        Report.date_submitted.desc()).paginate(per_page=5)
    return render_template('database.html', form=form, reports=reports, title="Database")


@app.route("/database/<string:username>")
def database_search(username):
    page = request.args.get("page", 1, type=int)
    if Report.query.filter_by(account_id=username).first() != None:
        reports = Report.query.filter_by(account_id=username).order_by( # returns list of all recently submitted reports
            Report.date_submitted.desc()).paginate(per_page=5)
    else:
        reports = None
    user_profile = scanning.get_twitter_info(username)
    return render_template('database_search.html', reports=reports, user_profile=user_profile, title="Database Search")


@app.route("/database/report_ranked")
def report_ranked():
    page = request.args.get("page", 1, type=int)
    count = db.session.query(Report.account_id, func.count(Report.account_id).label(
        "total")).group_by(Report.account_id)  # this gets the total reports grouped by account, ordered by total reports
    # it is a list of tuples (screen_name, count)
    count = count.order_by(desc('total'))
    # this variable is just a paginated version of count^
    counts2 = count.paginate(per_page=5)
    user_profiles = []
    for tup in count:  # for tuple in count variable
        # get the twitter profile of the screen_name
        user_profile = scanning.get_twitter_info(tup[0])
        user_profiles.append(user_profile)  # add it to a list
    length = len(user_profiles)
    return render_template('report_ranked.html', count=count, counts2=counts2, user_profiles=user_profiles, length=length, page=page, title="Reports Ranked")


@app.route("/database/my_reports")
@login_required
def my_reports():
    author = User.query.filter_by(username=current_user.username).first()
    page = request.args.get("page", 1, type=int)
    if Report.query.filter_by(author=author).first() != None:
        reports = Report.query.filter_by(author=author).order_by(
            Report.date_submitted.desc()).paginate(per_page=5)
    else:
        reports = None
    user_profile = scanning.get_twitter_info(author.username)
    return render_template('database_search.html', reports=reports, user_profile=user_profile, title="My Reports")


@app.route("/database/<string:username>/<int:report_id>/delete", methods=["POST"])
@app.route("/database/my_reports/<int:report_id>/delete", methods=["POST"])
@login_required
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash('Report Withdrawn!', 'info')
    return redirect(url_for("my_reports"))


@app.route('/unfollow_user/<string:screen_name>', methods=['GET', 'POST'])
def unfollow_user(screen_name):
    try:
        scanning.unfollow_user(screen_name) # tries unfollowing user x and flashes success or failure.
        flash(f"User unfollowed!", "success")
    except:
        flash(f"Unable to unfollow user", "danger")
    return redirect(url_for("database_search", username=screen_name))


@app.route('/mute_user/<string:screen_name>', methods=['GET', 'POST'])
def mute_user(screen_name):
    try:
        scanning.mute_user(screen_name) # tries muting user x and flashes success or failure.
        flash(f"User Muted!", "success")
    except:
        flash(f"Unable to mute user", "danger")
    return redirect(url_for("database_search", username=screen_name))


@app.route('/block_user/<string:screen_name>', methods=['GET', 'POST'])
def block_user(screen_name):
    try:
        scanning.block_user(screen_name) # tries block user x and flashes success or failure.
        flash(f"User blocked!", "success")
    except:
        flash(f"Unable to block user", "danger")
    return redirect(url_for("database_search", username=screen_name))
