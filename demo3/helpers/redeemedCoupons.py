from models import Redeemed_Coupons
from helpers.coupon import *
from helpers.restaurant import *

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


def get_redeemed_coupons_by_rid(rid):
    coupons = get_coupons(rid)

    for c in coupons:
        holders = Redeemed_Coupons.query.filter(Redeemed_Coupons.rid == rid, Redeemed_Coupons.cid == c['cid'], Redeemed_Coupons.valid == 1).count()
        used = Redeemed_Coupons.query.filter(Redeemed_Coupons.rid == rid, Redeemed_Coupons.cid == c['cid'], Redeemed_Coupons.valid == 0).count()
        c['holders'] = holders
        c['used'] = used

    return coupons


def mark_redeem_coupon_used_by_rcid(rcid):
    coupon = Redeemed_Coupons.query.filter(Redeemed_Coupons.rcid == rcid).first()
    coupon.valid = 0
    db.session.commit()
    return coupon

def find_rcid_by_cid_and_uid(cid, uid):
    coupon = Redeemed_Coupons.query.filter(Redeemed_Coupons.cid == cid, Redeemed_Coupons.uid == uid).first()
    if coupon:
        return coupon.rcid
    return "Not Found"


def get_redeemed_coupons_by_uid(uid):
    coupons = Redeemed_Coupons.query.filter(Redeemed_Coupons.uid == uid, Redeemed_Coupons.valid == 1).all()
    coupon_list = []

    for c in coupons:
        dict = get_coupon_by_cid(c.cid)

        dict["rname"] = get_restaurant_name_by_rid(c.rid)
        dict["raddress"] = get_restaurant_address(c.rid)
        coupon_list.append(dict)

    return coupon_list
