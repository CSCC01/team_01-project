from models import Restaurant, Employee, Achievements
from sqlalchemy import func

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
    name = name.lower()
    restaurants = Restaurant.query.filter(func.lower(Restaurant.name).contains(name))
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


def get_resturant_by_rid(rid):
    """
    Fetches a resturant from the Restaurant table.

    Retrives the restaurant with the given rid from the Restaurant table.

    Args:
        rid: The unique ID of the restaurant. An integer.

    Returns:
        A restaurant from the Restaurant table whose restaurant ID matches the
        given rid, or None if the restaurant does not exist.
    """
    return Restaurant.query.filter(Restaurant.rid == rid).first()

def update_restaurant_information(restaurant, name, address):
    """
    Updates the name and adress of a restaurant in the Restaurant table.

    Args:
        testaurant: The restaurant whose name is to be updated.
        name: The new name of the restaurant. A string.
        address: The new address of the restaurant. A string.

    Returns:
        A list of error messages, an empty list if there are no errors.
    """
    errmsg = []
    if len(name) < 1:
        errmsg.append("The restaurant's name cannot be empty.")
    if len(address) < 1:
        errmsg.append("The restaurant's address cannot be empty.")

    if not errmsg:
        restaurant.name = name
        restaurant.address = address
        db.session.commit()
    return errmsg

def get_restaurant_address(rid):
    """
    Get the restaurant address by the given rid

    Args:
        rid: The unique ID of the restaurant. An integer.

    Returns:
        (if found) restaurant address
        (if not) None
    """
    r = Restaurant.query.filter(Restaurant.rid == rid).first()
    if r != None:
        return r.address
    else:
        return None

def verify_scan_list(rid):
    """
    Return a list of uid which has access to scan in certain restaurant by the given rid

    Args:
        rid: The unique ID of the restaurant. An integer.

    Returns:
        a list of uid, only users whose uid in this list has access to scan in this restaurant
    """
    access = []
    r = Restaurant.query.filter(Restaurant.rid == rid).first()
    access.append(r.uid)
    employees = Employee.query.filter(Employee.rid == rid).all()
    for e in employees:
        access.append(e.uid)
    return access

def get_rid_by_aid(aid):
    """
    Return the rid by the given aid

    Args:
        aid: The unique ID of the achievement. An integer.

    Returns:
        (if found) the restaurant id
        (if not) 'Not Found'
    """
    a = Achievements.query.filter(Achievements.aid == aid).first()
    if a:
        return a.rid
    return "Not Found"

def get_errmsg_registration(rname, address, errmsg):
    """
    Returns a list of errmsg that occur when insering an owner account

    Args:
        rname: The name of the restaurant. A string.
        address: The address of the restaurant. A string.
        errmsg: Any preexisting error messages. A list of strings.
    Returns:
        A list of error messages. A list of strings.
    """
    if rname == "":
        errmsg.append("A restaurant name is required.")
    if address == "":
        errmsg.append("A restaurant address is required.")

    return errmsg
