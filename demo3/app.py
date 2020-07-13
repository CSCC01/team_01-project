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
        return render_template('home.html', owner = Restaurant.query.filter(Restaurant.uid == session['account']).first())
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

    # An list of all the errors that will be displayed to the user if login fails
    errmsg = []
    if request.method == 'POST':
        # Grabs information from signup fields
        name = request.form['name']
        email = request.form['email']
        password = (hashlib.md5(request.form['password'].encode())).hexdigest()
        password2 = (hashlib.md5(request.form['password2'].encode())).hexdigest()

        # Checks if email already exist and passwords are the same
        user = User.query.filter(User.email == email).first()
        if user:
            errmsg.append("Email has already been used.")
        if password != password2:
            errmsg.append("Passwords do not match.")

        # Adds user to db if no resistration errors occured
        if user == None and password == password2:
            user = User(name=name, email=email, password=password, type = -1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template("registration0.html", errmsg=errmsg)


# Owner register
@app.route('/registration1', methods=['GET', 'POST'])
@app.route('/registration1.html', methods=['GET', 'POST'])
def owner_register():
    # If someone is already logged in they get redirected to the home page
    if 'account' in session:
        return redirect(url_for('home'))

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
            user = User(name = name, email = email, password = password, type = 1)
            db.session.add(user)
            db.session.commit()

            restaurant = Restaurant(name = rname, address=address, uid = user.uid)
            db.session.add(restaurant)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template("registration1.html", errmsg=errmsg)


# Employee registration
@app.route('/registration2', methods=['GET', 'POST'])
@app.route('/registration2.html', methods=['GET', 'POST'])
def employee_register():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))

    # If an owner is logged in, get it
    owner = Restaurant.query.filter(Restaurant.uid == session['account']).first()
    # Page is restricted to owners only, if user is not an owner, redirect to home page
    if not owner:
        return redirect(url_for('home'))

    # An list of all the errors that will be displayed to the user if login fails
    errmsg = []
    if request.method == 'POST':
        # Grabs information from signup fields
        name = request.form['name']
        email = request.form['email']
        password = (hashlib.md5(request.form['password'].encode())).hexdigest()
        password2 = (hashlib.md5(request.form['password2'].encode())).hexdigest()

        # Checks if email already exist and passwords match
        user = User.query.filter(User.email == email).first()
        if user:
            errmsg.append("Email has already been used.")
        if password != password2:
            errmsg.append("Passwords do not match.")

        if user == None and password == password2:
            user = User(name = name, email = email, password = password, type = 0)
            db.session.add(user)
            db.session.commit()

            # Get the rid of the restaurant owner creating the account
            rid = Restaurant.query.filter(Restaurant.uid == session['account']).first().rid

            employee = Employee(uid = user.uid, rid = rid)
            db.session.add(employee)
            db.session.commit()
            return redirect(url_for('employee'))

    return render_template("registration2.html", errmsg=errmsg, owner = owner)


# Coupon page
@app.route('/coupon.html')
@app.route('/coupon')
def coupon():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))

    owner = Restaurant.query.filter(Restaurant.uid == session['account']).first()
    if (owner):
        rid = Restaurant.query.filter(Restaurant.uid == session['account']).first().rid
        return render_template("coupon.html",
            owner = Restaurant.query.filter(Restaurant.uid == session['account']).first(),
            coupons = Coupon.query.filter(Coupon.rid == rid).all())
    else:
        return render_template("coupon.html", owner = Restaurant.query.filter(Restaurant.uid == session['account']).first())


@app.route('/createCoupon.html', methods=['GET', 'POST'])
@app.route('/createCoupon', methods=['GET', 'POST'])
def create_coupon():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))

    # If an owner is logged in, get it
    owner = Restaurant.query.filter(Restaurant.uid == session['account']).first()
    # Page is restricted to owners only, if user is not an owner, redirect to home page
    if not owner:
        return redirect(url_for('home'))

    errmsg = []

    if request.method == 'POST':
        # Grabs information from coupon fields
        name = request.form['name']
        rid = Restaurant.query.filter(Restaurant.uid == session['account']).first().rid
        points = request.form['points']
        description = request.form['description']
        expiration = request.form['end']
        begin = request.form['begin']
        # true -> no expiration date, false -> expiration date required
        indefinite = "indefinite" in request.form

        if points == "" or int(points) < 0:
            errmsg.append("Invalid amount for points.")
        if name == "":
            errmsg.append("Invalid coupon name, please give your coupon a name.")
        if not indefinite and (expiration == "" or begin == ""):
            errmsg.append("Missing start or expiration date.")
        if points != "" and int(points) >= 0 and name != "" and (indefinite or (expiration != "" and begin != "")):
            if indefinite:
                coupon = Coupon(rid = rid, name = name, points = points, description = description)
            else:
                coupon = Coupon(rid = rid, name = name, points = points, description = description, expiration = expiration, begin = begin)
            db.session.add(coupon)
            db.session.commit()
            return redirect(url_for('coupon'))

        return render_template('createCoupon.html', owner = Restaurant.query.filter(Restaurant.uid == session['account']).first(), errmsg = errmsg,
                            info = {'name': name, 'points': points, 'description': description, 'expiration': expiration, 'begin': begin})
    else:
        return render_template('createCoupon.html', owner = Restaurant.query.filter(Restaurant.uid == session['account']).first())


@app.route('/employee.html', methods=['GET', 'POST'])
@app.route('/employee', methods=['GET', 'POST'])
def employee():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))

    owner = Restaurant.query.filter(Restaurant.uid == session['account']).first()
    if owner:
        if request.method == 'POST':
            # Deletes employee from employee table
            Employee.query.filter(Employee.uid == request.form['user']).delete()
            db.session.commit()
            # Deletes employee from user table
            User.query.filter(User.uid == request.form['user']).delete()
            db.session.commit()

        rid = Restaurant.query.filter(Restaurant.uid == session['account']).first().rid
        employees = Employee.query.filter(Employee.rid == rid).all()
        employee_list = []
        for employee in employees:
            e = User.query.filter(User.uid == employee.uid).first()
            employee_list.append(e)

        return render_template("employee.html",
                               owner = Restaurant.query.filter(Restaurant.uid == session['account']).first(),
                               employees = employee_list)
    else:
        return redirect(url_for('home'))

@app.route('/search.html', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def search():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))
    customer = User.query.filter(User.uid == session['account']).first().type

    if customer != -1:
        return redirect(url_for('home'))

    if request.method == 'POST':
        query = request.form['query']
        return render_template('search.html', restaurants = Restaurant.query.filter(Restaurant.name.contains(query)), query = request.form['query'])
    else:
        return render_template('search.html')


@app.route('/profile.html')
@app.route('/profile')
def profile():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))
    else :
        return render_template('profile.html', owner = Restaurant.query.filter(Restaurant.uid == session['account']).first())


# To end session you must logout
@app.route('/logout')
@app.route('/logout.html')
def logout():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login'))
    else:
        session.pop('account', None)
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
