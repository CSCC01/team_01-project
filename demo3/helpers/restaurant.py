from models import Restaurant

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


def insert_new_restaurant(rname, address, uid):
    """
    Inserts restaurant into restaurant table.

    Args:
        rname: The name given to the resturant. A string with max 64 characters.
        address: The address given to the resturant. A string with max 64
          characters.
        uid: The user ID that corressponds to the a owner. A positive integer.

    Returns:
        the resturant ID that corressponds with the newly inserted restaurant.
        The resturant ID is always a positive interger.
    """
    restaurant = Restaurant(name = rname, address=address, uid = uid)
    db.session.add(restaurant)
    db.session.commit()
    return restaurant.rid


def get_rid(uid):
    """
    Fetches a row from the Restaurant table.

    Retrieves a row pertaining the given user ID from the Restaurant table in
    the database.

    Args:
        uid: The user ID that corressponds to the Restaurant that is fetched.
          A positive integer.

    Returns:
        The ID of the restaurant that corresponds with the given user ID, None
        if no such restaurant exists.
    """
    owner = Restaurant.query.filter(Restaurant.uid == uid).first()
    if owner:
        return owner.rid
    return None


def get_resturant_by_name(name):
    """
    Fetches a list of resturants from the Restaurant table.

    Retrives a list of restaurants containing the substring name from the
    Restaurant table.

    Args:
        name: The substring that is searched for. A string.

    Returns:
        A list containing all restaurants from the Restaurant table whose name
        has the substring of the provided name within it.
    """
    restaurants = Restaurant.query.filter(Restaurant.name.contains(name))
    res_list = []
    for r in restaurants:
        dict = {
            "name": r.name,
            "address": r.address,
            "rid": r.rid
        }
        res_list.append(dict)
    return res_list


def get_restaurant_name_by_rid(rid):
    """
    Fetches a row from the Resturant table.

    Args:
        rid: The restaurant ID that corressponds to the Restaurant that is fetched.
          A positive integer.

    Returns:
        The name of a restaurant that corresponds to the givem rid, None otherise.
    """
    r = Restaurant.query.filter(Restaurant.rid == rid).first()
    if r != None:
        return r.name
    else:
        return None
