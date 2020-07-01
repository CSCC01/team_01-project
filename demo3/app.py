# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session
from exts import db
from models import User, Coupon
import config
import hashlib
import os

app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)


@app.route('/home.html')
def index():
    return render_template('home.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    errmsg = []
    if request.method == 'GET':
        return render_template('login.html')
    elif 'user_id' in session:
        return redirect(url_for('home'))
    else:
        email=request.form.get('email')
        password=request.form.get('password')
        user = User.query.filter(User.email==email, User.password_hash==password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return render_template("home.html")
        else:
            errmsg.append("incorrect email or password")
            return render_template("login.html", errmsg = errmsg)


# @app.route('/', methods = ['GET', 'POST'])
# @app.route('/login.html', methods = ['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # builds a dictinary with the input taken from the login fields
#         validationInfo = {
#             'email': request.form['email'],
#             'password': (hashlib.md5(request.form['password'].encode())).hexdigest()
#         }
#         # Builds a user from login credentials
#         user = buildUser(validationInfo)
#         # creates a session with the given information
#         if "uid" in user:
#             session['account'] = user['uid']
#             return render_template("home.html")
#
#     # User is already signed up, redirects them to the home page
#     elif 'account' in session:
#         return redirect(url_for('home'))
#
#     # Info is invalid or nothing has been submitted
#     return render_template("login.html")


# The home landing pages
@app.route('/home.html')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


# The registration options page
@app.route('/registration.html')
def registration():
    return render_template('registration.html')


# user register
@app.route('/registration0.html', methods=['GET', 'POST'])
def user_register():
    errmsg = []
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        address = request.form.get('address')
        name = request.form.get('name')
        if not (email or password or password2 or address or name):
            errmsg.append("Please fill all required information")
        else:
            # check if email already exist
            user = User.query.filter(User.email == email).first()
            if user:
                errmsg.append("Email has already been used.")
            else:
                if password==password2:
                    user = User(name=name, email=email, password_hash=password, address=address, exp=1, user_type=-1)
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('login'))
                else:
                    errmsg.append("Passwords do not match.")

    return render_template("registration0.html", errmsg=errmsg)


# @app.route('/owner/register', methods=['GET', 'POST'])
# def owner_register():
#     if request.method == 'GET':
#         return render_template('registration0.html')
#     else:
#         email = request.form.get('email')
#         password = request.form.get('password')
#         address = request.form.get('restaurantAddress')
#         name = request.form.get('name')
#
#         # check if email already exist
#         user = User.query.filter(User.email == email).first()
#         if user:
#             return 'this email has already been registered'
#         else:
#             user = User(name=name, email=email, password_hash=password, address=address, exp=-1, user_type=1)
#             db.session.add(user)
#             db.session.commit()
#             return redirect(url_for('login'))

# owner register
@app.route('/registration1.html', methods=['GET', 'POST'])
def owner_register():
    errmsg = []
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        address = request.form.get('address')
        name = request.form.get('name')
        # rname = request.form.get('rname')
        # write more
        if not (email or password or password2 or address or name):
            errmsg.append("Please fill all required information")
        else:
            # check if email already exist
            user = User.query.filter(User.email == email).first()
            if user:
                errmsg.append("Email has already been used.")
            else:
                if password == password2:
                    user = User(name=name, email=email, password_hash=password, address=address, exp=-1, user_type=1)
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('login'))
                else:
                    errmsg.append("Passwords do not match.")

    return render_template("registration1.html", errmsg=errmsg)


# Coupon page
# uncompleted
@app.route('/coupon.html')
def coupon():
    # coupons = getCouponsById({'uid': session['account']})
    # return render_template("coupon.html", owner = coupons != [], coupons = coupons)
    # We need a user_coupon column

    return render_template("coupon.html")


@app.route('/createCoupon.html', methods=['GET', 'POST'])
def create_coupon():
    errmsg = []
    if request.method == 'GET':
        return render_template('createCoupon.html')
    else:
        name = request.form.get('name')
        discount = request.form.get('discount')
        description = request.form.get('description')
        date = request.form.get('date')
        if not (name or discount or date):
            errmsg.append("Missing required information")
        else:
            coupon = Coupon(name=name, amount=discount, description=description, date=date)
            db.session.add(coupon)
            db.session.commit()

    return redirect(url_for('coupon'))


# To end session you must logout
@app.route('/logout')
def logout():
    session.pop('account', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()

