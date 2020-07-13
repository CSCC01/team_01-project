#################################
#                               #
#   Getters from the database   #
#                               #
#################################
from models import User, Coupon, Restaurant, Employee


"""Returns a user if valid credentials, None otherwise"""
def get_user_login(email, password):
    user = User.query.filter(User.email == email, User.password == password).first()
    return user


"""Returns the rid associated with a uid, None otherwise"""
def get_rid(uid):
    owner = Restaurant.query.filter(Restaurant.uid == uid).first()
    if owner:
        return owner.rid
    return None


"""Returns a list of all coupons from a restaurant with rid"""
def get_coupons(rid):
    coupon_list = []
    coupons = Coupon.query.filter(Coupon.rid == rid).all()
    for c in coupons:
        dict = {
            "cid": c.cid,
            "name": c.name,
            "description": c.description,
            "points": c.points,
            "begin": c.begin,
            "expiration": c.expiration
        }
        coupon_list.append(dict)
    return coupon_list


"""Returns a list of all employees that work the resturant with rid"""
def get_employees(rid):
    employee_list = []
    employees = Employee.query.filter(Employee.rid == rid).all()
    for e in employees:
        employee = User.query.filter(User.uid == e.uid).first()
        dict = {
            "uid": employee.uid,
            "name": employee.name,
            "email": employee.email
        }
        employee_list.append(dict)
    return employee_list


"""Returns a list of resturants that contains name in the name"""
def get_resturant_by_name(name):
    return Restaurant.query.filter(Restaurant.name.contains(name))
