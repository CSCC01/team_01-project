# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session
import config
from exts import db
from models import User, Coupon

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email=request.form.get('email')
        password=request.form.get('password')
        user = User.query.filter(User.email==User.email, User.password_hash ==password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return "incorrect email or password!"



@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        return render_template('registration1.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        address = request.form.get('address')
        name = request.form.get('name')

        # check if email already exist
        user = User.query.filter(User.email == email).first()
        if user:
            return 'this email has already been registered'
        else:
            user = User(name=name, email=email, password_hash=password, address=address, exp=1, user_type=-1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/owner/register', methods=['GET', 'POST'])
def owner_register():
    if request.method == 'GET':
        return render_template('registration0.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        address = request.form.get('restaurantAddress')
        name = request.form.get('name')

        # check if email already exist
        user = User.query.filter(User.email == email).first()
        if user:
            return 'this email has already been registered'
        else:
            user = User(name=name, email=email, password_hash=password, address=address, exp=-1, user_type=1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/coupon/create', methods=['GET', 'POST'])
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
        return redirect(url_for('create_coupon'))


if __name__ == '__main__':
    app.run()
