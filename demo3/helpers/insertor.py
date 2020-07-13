#################################
#                               #
#   Setters from the database   #
#                               #
#################################
from models import User, Coupon, Restaurant, Employee
from exts import db
import hashlib

"""
Inserts a new user into the user table

Returns error messages if an account cannot be created and uid if an account was created
"""
def insert_new_user(name, email, password1, password2, type):
    errmsg = []

    user = User.query.filter(User.email == email).first()
    if user:
        errmsg.append("Email has already been used.")
    if password1 != password2:
        errmsg.append("Passwords do not match.")
    if email == "":
        errmsg.append("An email is required")
    if password1 == (hashlib.md5("".encode())).hexdigest():
        errmsg.append("A password is required")

    # Adds user to db if no resistration errors occured
    if not errmsg:
        user = User(name=name, email=email, password=password1, type = type)
        db.session.add(user)
        db.session.commit()
        return None, user.uid

    return errmsg, None


"""
Inserts restaurant into restaurant table

Returns None if a restaurant was successfully registered
"""
def insert_new_restaurant(rname, address, uid):
    restaurant = Restaurant(name = rname, address=address, uid = uid)
    db.session.add(restaurant)
    db.session.commit()
    return restaurant.rid

"""
Inserts employee into employee table

Returns None if successfully registered
"""
def insert_new_employee(uid, rid):
    employee = Employee(uid = uid, rid = rid)
    db.session.add(employee)
    db.session.commit()
    return None


"""
Inserts a valid coupon into the database

Returns a list of error messages if insert is unsuccessful, None otherwise
"""
def insert_coupon(rid, name, points, description, begin, expiration, indefinite):
    errmsg = []

    if points == "" or int(points) < 0:
        errmsg.append("Invalid amount for points.")
    if name == "":
        errmsg.append("Invalid coupon name, please give your coupon a name.")
    if not indefinite and (expiration == "" or begin == ""):
        errmsg.append("Missing start or expiration date.")

    if not errmsg:
        if indefinite:
            coupon = Coupon(rid = rid, name = name, points = points, description = description)
        else:
            coupon = Coupon(rid = rid, name = name, points = points, description = description, expiration = expiration, begin = begin)
        db.session.add(coupon)
        db.session.commit()
        return None

    return errmsg
