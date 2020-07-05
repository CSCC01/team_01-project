# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session
from exts import db
from models import User, Coupon, Restaurant, Employee
import config
import os
import hashlib

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
        user = User.query.filter(User.email == email, User.password == password).first()
        if user:
            session['account'] = user.uid
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
def registration():
    return render_template('registration.html')


# Customer register
@app.route('/registration0', methods=['GET', 'POST'])
@app.route('/registration0.html', methods=['GET', 'POST'])
def user_register():
    # An list of all the errors that will be displayed to the user if login fails
    errmsg = []
    if request.method == 'POST':
        # Grabs information from signup fields
        name = request.form['name']
        email = request.form['email']
        password = (hashlib.md5(request.form['password'].encode())).hexdigest()
        password2 = (hashlib.md5(request.form['password2'].encode())).hexdigest()
        address = request.form['address']

        # Checks if email already exist and passwords are the same
        user = User.query.filter(User.email == email).first()
        if user:
            errmsg.append("Email has already been used.")
        if password != password2:
            errmsg.append("Passwords do not match.")

        # Adds user to db if no resistration errors occured
        if user == None and password == password2:
            user = User(name=name, email=email, password=password, address=address, type = -1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template("registration0.html", errmsg=errmsg)


# Owner register
@app.route('/registration1', methods=['GET', 'POST'])
@app.route('/registration1.html', methods=['GET', 'POST'])
def owner_register():
    # An list of all the errors that will be displayed to the user if login fails
    errmsg = []
    if request.method == 'POST':
        # Grabs information from signup fields
        name = request.form['name']
        email = request.form['email']
        password = (hashlib.md5(request.form['password'].encode())).hexdigest()
        password2 = (hashlib.md5(request.form['password2'].encode())).hexdigest()
        address = request.form['address']
        rname = request.form['rname']

        # Checks if email already exist and passwords match
        user = User.query.filter(User.email == email).first()
        if user:
            errmsg.append("Email has already been used.")
        if password != password2:
            errmsg.append("Passwords do not match.")

        if user == None and password == password2:
            user = User(name = name, email = email, password = password, address = address, type = 1)
            db.session.add(user)
            db.session.commit()

            restaurant = Restaurant(name = rname, uid = user.uid)
            db.session.add(restaurant)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template("registration1.html", errmsg=errmsg)


# Employee registration
@app.route('/registration2', methods=['GET', 'POST'])
@app.route('/registration2.html', methods=['GET', 'POST'])
def employee_register():
    # An list of all the errors that will be displayed to the user if login fails
    errmsg = []
    if request.method == 'POST':
        # Grabs information from signup fields
        name = request.form['name']
        email = request.form['email']
        password = (hashlib.md5(request.form['password'].encode())).hexdigest()
        password2 = (hashlib.md5(request.form['password2'].encode())).hexdigest()
        address = request.form['address']

        # Checks if email already exist and passwords match
        user = User.query.filter(User.email == email).first()
        if user:
            errmsg.append("Email has already been used.")
        if password != password2:
            errmsg.append("Passwords do not match.")

        if user == None and password == password2:
            user = User(name = name, email = email, password = password, address = address, type = 0)
            db.session.add(user)
            db.session.commit()

            # Get the rid of the restaurant owner creating the account
            rid = Restaurant.query.filter(Restaurant.uid == session['account']).first().rid

            employee = Employee(uid = user.uid, rid = rid)
            db.session.add(employee)
            db.session.commit()
            return redirect(url_for('profile'))

    return render_template("registration2.html", errmsg=errmsg)

# Employee page
@app.route('/employee.html', methods=['GET', 'POST'])
@app.route('/employee', methods=['GET', 'POST'])
def employee():
    owner = Restaurant.query.filter(Restaurant.uid == session['account']).first()
    if owner:
        rid = Restaurant.query.filter(Restaurant.uid == session['account']).first().rid
        employeeID = []
        for employee in Employee.query.filter(Restaurant.rid == rid):
            employeeID.append(employee.uid)
        return render_template("employee.html",
                               owner=Restaurant.query.filter(Restaurant.uid == session['account']).first(),
                               employee=User.query.filter(User.uid.in_((employeeID))))
    else:
        return redirect(url_for('accessForbidden'))
    
# Coupon page
@app.route('/coupon.html')
@app.route('/coupon')
def coupon():
    owner = Restaurant.query.filter(Restaurant.uid == session['account']).first()
    if (owner):
        rid = Restaurant.query.filter(Restaurant.uid == session['account']).first().rid
        return render_template("coupon.html",
            owner = Restaurant.query.filter(Restaurant.uid == session['account']).first(),
            coupons = Coupon.query.filter(Coupon.rid == rid).all())
    else:
        return render_template("coupon.html")


@app.route('/createCoupon.html', methods=['GET', 'POST'])
@app.route('/createCoupon', methods=['GET', 'POST'])
def create_coupon():
    if request.method == 'POST':
        # Grabs information from coupon fields
        name = request.form['name']
        rid = Restaurant.query.filter(Restaurant.uid == session['account']).first().rid
        discount = request.form['discount']
        description = request.form['description']
        expiration = request.form['end']
        begin = request.form['begin']

        # Inserts coupon info to db -- currently input is NOT sanitized
        coupon = Coupon(rid = rid, name = name, discount = discount, description = description, expiration = expiration, begin = begin)
        db.session.add(coupon)
        db.session.commit()
        return redirect(url_for('coupon'))
    else:
        return render_template('createCoupon.html')


@app.route('/profile.html')
@app.route('/profile')
def profile():
    return render_template('profile.html', owner = Restaurant.query.filter(Restaurant.uid == session['account']).first())


# To end session you must logout
@app.route('/logout')
@app.route('/logout.html')
def logout():
    session.pop('account', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
