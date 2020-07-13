#################################
#                               #
#  Updators from the database   #
#                               #
#################################
from models import User, Coupon, Restaurant, Employee
import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db

"""
Returns None

Deletes a coupon with cid
"""
def delete_coupon(cid):
    Coupon.query.filter(Coupon.cid == cid).delete()
    db.session.commit()
    return None

def delete_employee(uid):
    # Deletes employee from employee table
    Employee.query.filter(Employee.uid == uid).delete()
    db.session.commit()
    # Deletes employee from user table
    User.query.filter(User.uid == uid).delete()
    db.session.commit()
