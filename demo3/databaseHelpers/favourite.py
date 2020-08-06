from models import Favourite
from databaseHelpers.restaurant import *

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


def add_favourite(uid, rid):
    """
    Inserts a row into the Favourite table.

    Args:
        uid: A user ID that corresponds to a user in the User table. A integer.
        rid: A restaurant ID that corresponds to a restaurant in the Restaurant
          table. A integer.

    Returns:
        None.
    """
    fav = Favourite(uid = uid, rid = rid)
    db.session.add(fav)
    db.session.commit()

def check_favourite(uid, rid):
    """
    Searches for a row with the corresponding uid and rid in the Favourite table.

    Args:
        uid: A user ID that corresponds to a user in the User table. A integer.
        rid: A restaurant ID that corresponds to a restaurant in the Restaurant
          table. A integer.

    Returns:
        True if a favourite was found with matching uid and rid. False otherwise.
    """
    fav = Favourite.query.filter(Favourite.uid == uid, Favourite.rid == rid).first()
    return fav != None

def get_favourites(uid):
    """
    Fetches for all rows with corresponding uid and rid in the Favourite table.

    Args:
        uid: A user ID that corresponds to a user in the User table. A integer.
        rid: A restaurant ID that corresponds to a restaurant in the Restaurant
          table. A integer.

    Returns:
        A list of restaurants that are favourited
    """
    fav = Favourite.query.filter(Favourite.uid == uid).all()
    fav_list = []
    for f in fav:
        dict = {
            "rid": f.rid,
            "name": get_restaurant_name_by_rid(f.rid),
            "address": get_restaurant_address(f.rid)
        }
        fav_list.append(dict)
    return fav_list

def remove_faviourite(uid, rid):
    """
    Removes a row from the Favourite table.

    Args:
        uid: A user ID that corresponds to a user in the User table. A integer.
        rid: A restaurant ID that corresponds to a restaurant in the Restaurant
          table. A integer.

    Returns:
        None.
    """
    fav = Favourite.query.filter(Favourite.uid == uid, Favourite.rid == rid).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
