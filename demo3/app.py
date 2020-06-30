# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session
from exts import db
from models import User, Coupon
import config
import os

app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)


@app.route('/home.html')
def index():
    return render_template('home.html')


@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email=request.form.get('email')
        password=request.form.get('password')
        user = User.query.filter(User.email==email, User.password_hash ==password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return render_template("home.html")
        else:
            return "incorrect email or password!"


# The home landing pages
@app.route('/home.html')
def home():
    if 'account' in session:
        return render_template('home.html')
    else:
        return render_template('login.html')


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

        # check if email already exist
        user = User.query.filter(User.email == email).first()
        if user:
            errmsg.append("Email has already been used.")
        else:
            if password==password2:
                user = User(name=name, email=email, password_hash=password, address=address, exp=1, user_type=-1)
                db.session.add(user)
                db.session.commit()
                return render_template('login.html')
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
        rname = request.form.get('rname')
        # write more

        # check if email already exist
        user = User.query.filter(User.email == email).first()
        if user:
            errmsg.append("Email has already been used.")
        else:
            if password == password2:
                user = User(name=name, email=email, password_hash=password, address=address, exp=-1, user_type=1)
                db.session.add(user)
                db.session.commit()
                return render_template('login.html')
            else:
                errmsg.append("Passwords do not match.")

    return render_template("registration1.html", errmsg=errmsg)


# Coupon page
# uncompleted
@app.route('/coupon.html')
def coupon():
    # coupons = getCouponsById({'uid': session['account']})
    # return render_template("coupon.html", owner = coupons != [], coupons = coupons)
    return render_template("coupon.html")


@app.route('/createCoupon.html', methods=['GET', 'POST'])
def create_coupon():
    if request.method == 'GET':
        return render_template('createCoupon.html')
    else:
        name = request.form.get('name')
        discount = request.form.get('discount')
        description = request.form.get('description')
        date = request.form.get('date')

        coupon = Coupon(name=name, amount=discount, description=description, date=date)
        db.session.add(coupon)
        db.session.commit()
        return render_template("createCoupon.html")


# To end session you must logout
@app.route('/logout')
def logout():
    session.pop('account', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
