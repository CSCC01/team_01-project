from models import Redeemed_Coupons
from helpers.coupon import *

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


#def get_Redeemed_Coupons_by_rid(rid):
    """
    Fetches rows from the Redeemed_Coupons, user and coupon table.

    Retrieves all coupons that a specific restaurant has in circularion.

    Args:
        rid: A restaurant ID that corresponds to a restaurant in the
          Redeemed_Coupons table. A integer.

    Returns:
        A list of dictinaries that contains information about each coupon a
        customer has possession of at a specific resturant.

    coupons = Redeemed_Coupons.query.filter(Redeemed_Coupons.rid == rid).all()
    customer_coupon_list = []
    for c in coupons:
        user = User.query.filter(User.uid == c.uid).first()
        coupon = Coupon.query.filter(Coupon.cid == c.cid).first()
        dict = {
            "email": user.email,
            "cname": coupon.name,
            "begin": coupon.begin,
            "expiration": coupon.expiration,
            "description": coupon.description,
            "points": coupon.points
        }
        customer_coupon_list.append(dict)
    return customer_coupon_list"""


def get_redeemed_coupons_by_rid(rid):
    coupons = get_coupons(rid)

    for c in coupons:
        holders = Redeemed_Coupons.query.filter(Redeemed_Coupons.rid == rid, Redeemed_Coupons.cid == c['cid'], Redeemed_Coupons.valid == 1).count()
        used = Redeemed_Coupons.query.filter(Redeemed_Coupons.rid == rid, Redeemed_Coupons.cid == c['cid'], Redeemed_Coupons.valid == 0).count()
        c['holders'] = holders
        c['used'] = used

    return coupons
