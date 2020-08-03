from models import Experience
from databaseHelpers.restaurant import *

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


def get_restaurants_with_experience(uid):
    """"""
    restaurant_list = []
    exp = Experience.query.filter(Experience.uid == uid).order_by(Experience.experience).all()
    for e in exp:
        dict = {
            "rid": e.rid,
            "experience": e.experience,
            "name": get_restaurant_name_by_rid(e.rid),
            "address": get_restaurant_address(e.rid)
        }
        restaurant_list.append(dict)
    return restaurant_list
