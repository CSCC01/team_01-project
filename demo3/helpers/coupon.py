from models import Coupon, User
from datetime import date

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


def insert_coupon(rid, name, points, description, begin, expiration, indefinite):
    """
    Inserts a coupon into Coupon table.

    Args:
        rid: A restaurant ID that corresponds to a restaurant in the Restaurant
          table. A integer.
        name: A name for the coupon. A 64 character string.
        points: A point value for the coupon. A integer.
        description: A description of the coupon. A 1024 character string.
        begin: A starting date for the coupon. A DateTime.
        expiration: An ending date for the coupon. A DateTime.
        indefinite: A boolean with the following property:
          true == coupon has no begining/ending date.
          false == coupon has a begining/ending date.

    Returns:
        None if coupon was successfully added to the Coupon table, a list of
        error messages otherwise.
    """
    errmsg = []

    if points == "" or int(points) < 0:
        errmsg.append("Invalid amount for points.")
    if name == "":
        errmsg.append("Invalid coupon name, please give your coupon a name.")
    if not indefinite and (expiration == None or begin == None):
        errmsg.append("Missing start or expiration date.")

    if not errmsg:
        if indefinite:
            coupon = Coupon(rid = rid, name = name, points = points, description = description, deleted = 0)
        else:
            coupon = Coupon(rid = rid, name = name, points = points, description = description, expiration = expiration, begin = begin, deleted = 0)
        db.session.add(coupon)
        db.session.commit()
        return None

    return errmsg


def get_coupons(rid):
    """
    Fetches rows from the Coupon table.

    Retrieves a list of coupons from the Coupon table that belong to the
    restaurant with the given restaurant ID.

    Args:
        rid: A restaurant ID that corresponds to a restaurant in the Restaurant
          table. A integer.

    Returns:
        A list of coupons containing for a restaurant with restaurant ID that
        matches rid.
    """
    coupon_list = []
    coupons = Coupon.query.filter(Coupon.rid == rid).all()
    for c in coupons:
        dict = {
            "cid": c.cid,
            "name": c.name,
            "description": c.description,
            "points": c.points,
            "begin": c.begin,
            "expiration": c.expiration,
            "deleted": c.deleted
        }
        coupon_list.append(dict)
    return coupon_list



def delete_coupon(cid):
    """
    Removes a row from the Coupon table.

    Deletes a coupon from the database.

    Args:
        cid: A coupon ID that corresponds to a coupon in the Coupon table. A
          integer.

    Returns:
        None.
    """
    Coupon.query.filter(Coupon.cid == cid).delete()
    db.session.commit()
    return None


def filter_valid_coupons(coupons):
    """
    Removes invalid coupons from the coupons list.

    Deletes coupons that are either deleted or expired.

    Args:
        coupons: A list of dictinaries, each dictinary must have the keys,
          int 'deleted' and DateTime 'expiration'.

    Returns:
        A the list coupons with the invalid dictinaries removed.
    """
    today = date.today()
    for c in coupons:
        if c["deleted"] == 1 or (c["expiration"] != None and today > c["expiration"]):
            coupons.remove(c)

    return coupons


def get_coupon_by_cid(cid):

    coupon = Coupon.query.filter(Coupon.cid == cid).first()

    if coupon:
        c = {
            "cid": coupon.cid,
            "points": coupon.points,
            "cname": coupon.name,
            "cdescription": coupon.description,
            "begin": coupon.begin,
            "expiration": coupon.expiration
        }

        return c
    else:
        return None
