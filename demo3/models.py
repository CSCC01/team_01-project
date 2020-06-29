from exts import db
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_sqlalchemy import SQLAlchemy


# user_coupon = db.Table(
#     "user_coupon",
#     db.Column("user_id", db.Integer, db.ForeignKey("user_profile.id"), primary_key=True),
#     db.Column("coupon_id", db.Integer, db.ForeignKey("coupon_info.id"), primary_key=True)
# )


class User(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256), nullable=True)
    user_type = db.Column(db.Integer)
    exp = db.Column(db.Integer)   # experience
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
    __tablename__ = "coupon_info"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.DECIMAL(4, 2), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    date = db.Column(db.String(128), nullable=False)

