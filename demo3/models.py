from exts import db
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_sqlalchemy import SQLAlchemy


# user_coupon = db.Table(
#     "user_coupon",
#     db.Column("user_id", db.Integer, db.ForeignKey("user_profile.id"), primary_key=True),
#     db.Column("coupon_id", db.Integer, db.ForeignKey("coupon_info.id"), primary_key=True)
# )


class User(db.Model):
    __tablename__ = "user"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=True)
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
    discount = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)
    begin = db.Column(db.DateTime, nullable=False)

class Restaurant(db.Model):
    __tablename__ = "restaurant"
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    uid = db.Column(db.Integer)
    type = db.Column(db.Integer)
    # 1 for owner and 0 for employee
