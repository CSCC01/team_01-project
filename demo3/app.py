# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session
from helpers.user import *
from helpers.restaurant import *
from helpers.employee import *
from helpers.coupon import *
from helpers.redeemedCoupons import *
from helpers.points import *
from helpers.level import *
from datetime import date
import config
import os
import hashlib
import re
from helpers.qr_code import *

app = Flask(__name__)
app.secret_key = 'shhhh'

app.config.from_object(config)

db.init_app(app)

@app.route('/login', methods=['GET', 'POST'])
@app.route('/login.html', methods=['GET', 'POST'])
@app.route('/', methods = ['GET', 'POST'])
def login():
    # This runs when the user presses the login button
    if request.method == 'POST':
        # Grabs information from login feilds
        email =  request.form['email']
        password = (hashlib.md5(request.form['password'].encode())).hexdigest()

        # Validates that the user exits in the database
        # If the user exists in the databse, they are logged in
        # If the user does not exist in the database, the user is redirected to the login page with an errmsg
        user = get_user_login(email, password)
        if user:
            session['account'] = user.uid
            session['type'] = user.type
            session.permanent = True
            return redirect(url_for('home'))
        else:
            return render_template("login.html", errmsg = "Failed to login: Incorrect email or password")

    # This runs if the user is already in seassion
    # If the user is already in session, it redirectes them to their homepage
    elif 'account' in session:
        return redirect(url_for('home'))

    # This runs if the user is not in seassion
    # Displays the login page
    else:
        return render_template("login.html")


# The home landing page
# Currently nothing is here, buttons on nav bar work
@app.route('/home')
@app.route('/home.html')
def home():
    if 'account' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


# The registration options page
@app.route('/registration.html')
@app.route('/registration')
def registration():
    # If someone is already logged in they get redirected to the home page
    if 'account' in session:
        return redirect(url_for('home'))
    else:
        return render_template('registration.html')


# Customer register
@app.route('/registration0', methods=['GET', 'POST'])
@app.route('/registration0.html', methods=['GET', 'POST'])
def user_register():
    # If someone is already logged in they get redirected to the home page
    if 'account' in session:
        return redirect(url_for('home'))

    # A list of all the errors that will be displayed to the user if login fails
    errmsg = []
    if request.method == 'POST':
        # Grabs information from signup fields
        name = request.form['name']
        email = request.form['email']
        password = (hashlib.md5(request.form['password'].encode())).hexdigest()
        password2 = (hashlib.md5(request.form['password2'].encode())).hexdigest()

        errmsg, uid = insert_new_user(name, email, password, password2, -1)
        if not errmsg:
            return redirect(url_for('login'))
    return render_template("registration0.html", errmsg=errmsg)


# Owner register
@app.route('/registration1', methods=['GET', 'POST'])
@app.route('/registration1.html', methods=['GET', 'POST'])
def owner_register():
    # If someone is already logged in they get redirected to the home page
    if 'account' in session:
        return redirect(url_for('home'))

    # A list of all the errors that will be displayed to the user if login fails
    errmsg = []
    if request.method == 'POST':
        # Grabs information from signup fields
        name = request.form['name']
        email = request.form['email']
        password = (hashlib.md5(request.form['password'].encode())).hexdigest()
        password2 = (hashlib.md5(request.form['password2'].encode())).hexdigest()
        address = request.form['address']
        rname = request.form['rname']

        errmsg, uid = insert_new_user(name, email, password, password2, 1)

        if uid:
            insert_new_restaurant(rname, address, uid)
            return redirect(url_for('login'))

    return render_template("registration1.html", errmsg=errmsg)


# Employee registration
@app.route('/registration2', methods=['GET', 'POST'])
@app.route('/registration2.html', methods=['GET', 'POST'])
def employee_register():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))

    # Page is restricted to owners only, if user is not an owner, redirect to home page
    if session['type'] != 1:
        return redirect(url_for('home'))

    # An list of all the errors that will be displayed to the user if login fails
    errmsg = []
    if request.method == 'POST':
        # Grabs information from signup fields
        name = request.form['name']
        email = request.form['email']
        password = (hashlib.md5(request.form['password'].encode())).hexdigest()
        password2 = (hashlib.md5(request.form['password2'].encode())).hexdigest()

        errmsg, uid = insert_new_user(name, email, password, password2, 0)

        if uid:
            rid = get_rid(session["account"])
            insert_new_employee(uid, rid)
            return redirect(url_for('employee'))

    return render_template("registration2.html", errmsg=errmsg)


# Coupon page
@app.route('/coupon.html', methods=['GET', 'POST'])
@app.route('/coupon', methods=['GET', 'POST'])
def coupon():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))

    ### Customer viewing of coupons
    elif session["type"] == -1:
        if request.method == 'POST':
            cid = request.form['coupon']
            # imgurl = to_qr("https://pickeasy-beta.herokuapp.com/useCoupon/"+str(cid))
            imgurl = to_qr("http://127.0.0.1:5000/useCoupon/"+str(cid))
            return render_template("couponQR.html", imgurl=imgurl)
        coupons = get_redeemed_coupons_by_uid(session["account"])
        return render_template("coupon.html", coupons = coupons)

    # TODO: Employees view of the coupon page
    elif session["type"] == 0:
        return render_template("coupon.html")

    # Owners view of coupon page
    else:
        if request.method == 'POST':
            cid = request.form['coupon']
            delete_coupon(cid)

        rid = get_rid(session["account"])
        coupon_list = get_coupons(rid)

        return render_template("coupon.html", coupons = coupon_list)


@app.route('/createCoupon.html', methods=['GET', 'POST'])
@app.route('/createCoupon', methods=['GET', 'POST'])
def create_coupon():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))

    # Page is restricted to owners only, if user is not an owner, redirect to home page
    elif session['type'] != 1:
        return redirect(url_for('home'))

    errmsg = []

    if request.method == 'POST':
        # Grabs information from coupon fields
        name = request.form['name']
        points = request.form['points']
        description = request.form['description']
        expiration = request.form['end']
        begin = request.form['begin']
        # true -> no expiration date, false -> expiration date required
        indefinite = "indefinite" in request.form

        rid = get_rid(session["account"])
        errmsg = insert_coupon(rid, name, points, description, begin, expiration, indefinite)

        # Inserting was successful
        if not errmsg:
            return redirect(url_for('coupon'))

        # Inserting failed
        return render_template('createCoupon.html', errmsg = errmsg,
                            info = {'name': name, 'points': points, 'description': description, 'expiration': expiration, 'begin': begin})

    return render_template('createCoupon.html')

@app.route('/viewUserCoupons.html', methods=['GET', 'POST'])
@app.route('/viewUserCoupons', methods=['GET', 'POST'])
def viewUserCoupons():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))

    # Page is restricted to owners only, if user is not an owner, redirect to home page
    elif session['type'] != 1:
        return redirect(url_for('home'))

    rid = get_rid(session['account'])
    coupon_list = get_redeemed_coupons_by_rid(rid)
    today = date.today()
    return render_template("viewUserCoupons.html", coupons = coupon_list, today = today)

@app.route('/employee.html', methods=['GET', 'POST'])
@app.route('/employee', methods=['GET', 'POST'])
def employee():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))

    # Page is restricted to owners only, if user is not an owner, redirect to home page
    elif session['type'] != 1:
        return redirect(url_for('home'))

    if request.method == 'POST':
        uid = request.form['user']
        delete_employee(request.form['user'])

    rid = get_rid(session["account"])
    employee_list = get_employees(rid)

    return render_template("employee.html", employees = employee_list)


@app.route('/search.html', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def search():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))

    # Page is restricted to customers only, if user is not a customer, redirect to home page
    elif session['type'] != -1:
        return redirect(url_for('home'))

    if request.method == 'POST':
        if 'query' in request.form:
            query = request.form['query']
            restaurants = get_resturant_by_name(query)
            return render_template('search.html', restaurants = restaurants, query = request.form['query'])
        if 'rid' in request.form:
            rid = request.form['rid']
            return redirect(url_for('restaurant', rid=rid))
    else:
        return render_template('search.html')

@app.route('/restaurant<rid>.html', methods=['GET', 'POST'])
@app.route('/restaurant<rid>', methods=['GET', 'POST'])
def restaurant(rid):
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))

    # Page is restricted to customers only, if user is not a customer, redirect to home page
    elif session['type'] != -1:
        return redirect(url_for('home'))

    restaurant = get_resturant_by_rid(rid)
    if restaurant:
        # Gets coupons
        rname = get_restaurant_name_by_rid(rid)
        coupons = get_coupons(rid)

        # Gets point progress
        uid = session['account']
        if not get_points(uid, rid):
            insert_points(uid, rid)
        points = get_points(uid, rid).points
        level = convert_points_to_level(points)
        return render_template("restaurant.html", restaurant = restaurant, level = level,
                                overflow = get_points_since_last_level(level, points), rname = rname, coupons = coupons)
    else:
        return redirect(url_for('home'))


@app.route('/useCoupon/<cid>', methods=['GET', 'POST'])
def use_coupon(cid):
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))

    # Page is restricted to employee/owner only, if user is a customer, redirect to home page
    elif session['type'] == -1:
        return redirect(url_for('home'))

    # find rcid
    rcid = find_rcid_by_cid(cid)

    # mark used
    mark_redeem_coupon_used_by_rcid(rcid)

    return redirect(url_for('home'))


@app.route('/profile.html')
@app.route('/profile')
def profile():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))
    else :
        return render_template('profile.html')


# To end session you must logout
@app.route('/logout')
@app.route('/logout.html')
def logout():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))
    else:
        session.pop('account', None)
        session.pop('type', None)
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
