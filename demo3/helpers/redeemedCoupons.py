from models import Coupon, Customer_Coupons, User

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


def get_customer_coupons_by_rid(rid):
    """
    Fetches rows from the customer_coupons, user and coupon table.

    Retrieves all coupons that a specific restaurant has in circularion.

    Args:
        rid: A restaurant ID that corresponds to a restaurant in the
          Customer_Coupons table. A integer.

    Returns:
        A list of dictinaries that contains information about each coupon a
        customer has possession of at a specific resturant.
    """
    coupons = Customer_Coupons.query.filter(Customer_Coupons.rid == rid).all()
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
    return customer_coupon_list
