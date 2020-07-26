# from exts import db
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_sqlalchemy import SQLAlchemy


# user_coupon = db.Table(
#     "user_coupon",
#     db.Column("user_id", db.Integer, db.ForeignKey("user_profile.id"), primary_key=True),
#     db.Column("coupon_id", db.Integer, db.ForeignKey("coupon_info.id"), primary_key=True)
# )

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
if config.STATUS == "TEST":
    # for creating test
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db = SQLAlchemy(app)
else:
    from exts import db


class User(db.Model):
    __tablename__ = "user"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    type = db.Column(db.Integer)
    # coupons = db.relationship("Coupon", secondary=user_coupon)

    # @property
    # def password(self):
    #     raise AttributeError("not readable!")
    #
    # @password.setter
    # def password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)


class Coupon(db.Model):
    __tablename__ = "coupons"
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rid = db.Column(db.Integer)
    name = db.Column(db.String(64), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(64), nullable=False)
    expiration = db.Column(db.DateTime, nullable=True)
    begin = db.Column(db.DateTime, nullable=True)

class Restaurant(db.Model):
    __tablename__ = "restaurant"
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=True)
    uid = db.Column(db.Integer)

class Points(db.Model):
    __tablename__ = "points"
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer)
    rid = db.Column(db.Integer)
    points = db.Column(db.Integer)

class Employee(db.Model):
    __tablename__ = "employee"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rid = db.Column(db.Integer)

class Customer_Coupons(db.Model):
    __tablename__ = "customer_coupons"
    cid = db.Column(db.Integer, nullable=False, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, primary_key=True)
    rid = db.Column(db.Integer, nullable=False, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)

class Customer_AchievementProgress(db.Model):
    __tablename__ = "customer_achievement_progress"
    aid = db.Column(db.Integer, nullable=False, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, primary_key=True)
    progress = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
