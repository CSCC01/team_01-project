import sqlite3
import hashlib

from database.Builder import *
from flask import Flask, render_template, session, redirect, url_for, escape, request

DATABASE = 'database/pickeasy.db'

app = Flask(__name__)
app.secret_key = 'shhhh'


# This is for the login page
# If the user is already logged in a session, they will get redirected to their home page
# Function pulls information from the login fields and checks it with the database
@app.route('/', methods = ['GET', 'POST'])
@app.route('/login.html', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        # builds a dictinary with the input taken from the login fields
        validationInfo = {
            'email': request.form['email'],
            'password': (hashlib.md5(request.form['password'].encode())).hexdigest()
        }
        # Builds a user from login credentials
        user = buildUser(validationInfo)
        # creates a session with the given information
        if "uid" in user:
            session['account'] = user['uid']
            return render_template("home.html")

    # User is already signed up, redirects them to the home page
    elif 'account' in session:
        return redirect(url_for('home'))

    # Info is invalid or nothing has been submitted
    return render_template("login.html")


# The home landing pages
@app.route('/home.html')
def home():
    if 'account' in session:
        return render_template("home.html")
    else:
        return render_template("login.html")


# The registration options page
@app.route('/registration.html')
def registration():
    return render_template("registration.html")


# The customer registration pages
@app.route('/registration0.html', methods = ['GET', 'POST'])
def registration0():
    errmsg = []
    if request.method == 'POST':
        registrationInfo = {
            'tid': 0,
            'name': request.form['name'],
            'email': request.form['email'],
            'password': (hashlib.md5(request.form['password'].encode())).hexdigest(),
            'password2': (hashlib.md5(request.form['password2'].encode())).hexdigest(),
            'address': request.form['address']
        }
        user = getUserByEmail(registrationInfo)
        # Checks that email has been used and passwords match
        if (registrationInfo["password"] == registrationInfo["password2"] and "uid" not in user):
            insertUser(registrationInfo)
            return redirect(url_for('login'))

        # If passwords dont match, send an error message
        if (registrationInfo["password"] != registrationInfo["password2"]):
            errmsg.append("Passwords do not match.")
        # If email isnt unique, send an error message
        if ("uid" in user):
            errmsg.append("Email has already been used.")

    return render_template("registration0.html", errmsg = errmsg)


# The restaurant owners registration page
@app.route('/registration1.html', methods = ['GET', 'POST'])
def registration1():
    errmsg = []
    if request.method == 'POST':
        registrationInfo = {
            'tid': 1,
            'name': request.form['name'],
            'email': request.form['email'],
            'rname': request.form['rname'],
            'password': (hashlib.md5(request.form['password'].encode())).hexdigest(),
            'password2': (hashlib.md5(request.form['password2'].encode())).hexdigest(),
            'address': request.form['address']
        }
        user = getUserByEmail(registrationInfo)
        restaurant = getResturantByName(registrationInfo)
        # Checks that email has been used and passwords match
        if (registrationInfo["password"] == registrationInfo["password2"] and "uid" not in user and "rid" not in restaurant):
            insertUser(registrationInfo)
            user = getUserByEmail(registrationInfo)
            registrationInfo["uid"] = user["uid"]
            insertResturant(registrationInfo)
            return redirect(url_for('login'))

        # If passwords dont match, send an error message
        if (registrationInfo["password"] != registrationInfo["password2"]):
            errmsg.append("Passwords do not match.")
        # If email isnt unique, sends an error message
        if ("uid" in user):
            errmsg.append("Email has already been used.")
        # If restaurant name isnt unique, sends an error message
        if ("rid" in restaurant):
            errmsg.append("Restaurant name is already taken.")

    return render_template("registration1.html", errmsg = errmsg)


# Coupon page
@app.route('/coupon.html')
def coupon():
    coupons = getCouponsById({'uid': session['account']})
    return render_template("coupon.html", owner = coupons != [], coupons = coupons)


# Create a coupon page
@app.route('/createCoupon.html', methods = ['GET', 'POST'])
def createCoupon():
    if request.method == 'POST':
        couponInfo = {
            'name': request.form['name'],
            'rid': getRid({'uid': session['account']})['rid'],
            'amount': request.form['discount'],
            'description': request.form['description'],
            'expiration': request.form['date']
        }
        insertCoupon(couponInfo)
        return redirect(url_for('coupon'))

    return render_template("createCoupon.html")


# To end session you must logout
@app.route('/logout.html')
def logout():
    session.pop('account', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
