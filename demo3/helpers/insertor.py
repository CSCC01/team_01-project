#################################
#                               #
#   Setters from the database   #
#                               #
#################################
from models import User, Coupon, Restaurant, Employee
import config
import hashlib

if config.STATUS == "TEST":
    from models import db
else:
    from exts import db

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
        errmsg.append("An email is required.")
    # if password1 == (hashlib.md5("".encode())).hexdigest():
    if password1 == "":
        errmsg.append("A password is required.")

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
    if not indefinite and (expiration == None or begin == None):
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

"""
Inserts a valid achievement into the database

Returns error messages if insertion failed, none otherwise
"""
def insert_achievement(rid, name, description, experience, points, requireItem, requireFee, Item):
    errmsg = []

    if name == "":
        errmsg.append("Invalid achievement name, please provide an achieve name.")
    if description == "":
        errmsg.append("Invalid description of achievement, please provide a description.")
    if experience == "" and points == "":
        errmsg.append("Missing experience and points, please at least provide experience or points.")
    if int(experience) < 0:
        errmsg.append("Invalid experience, please provide non-negative value.")
    if int(points) < 0:
        errmsg.append("Invalid points, please provide non-negative value.")
    # if requireItem == "" and requireFee == "":
    #   errmsg.append("Missing experience and points, please at least provide one requirement.")
    if Item:
        if requireItem == "":
            errmsg.append("Missing experience.")
        if int(requireItem) < 0:
            errmsg.append("Invalid requirement, please provide non-negative value.")
    else:
        if requireFee == "":
            errmsg.append("Missing points.")
        if float(requireFee) < 0.0: 
            errmsg.append("Invalid requirement, please provide non-negative value.")
    
    if not errmsg:
        if Item:
            achievement = Achievement(rid = rid, name = name, description = description, experience = experience, points = points, requireItem = requireItem)
        else:
            achievement = Achievement(rid = rid, name = name, description = description, experience = experience, points = points, requireFee = requireFee)
        db.session.add(achievement)
        db.session.commit()
        return None
    else:
        return errmsg

