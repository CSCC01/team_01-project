from models import Points

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


def insert_points(uid, rid):
    """
    Inserts a 0 points entry into Points table for a given user and restaurant.

    Args:
        uid: A user ID that corresponds to a user in the User
          table. A integer.
        rid: A restaurant ID that corresponds to a restaurant in the Restaurant
          table. A integer.

    Returns:
        Points if entry was successfully added to the Points table, a list of
        error messages otherwise.
    """
    errmsg = []

    points = Points.query.filter(Points.uid == uid).filter(Points.rid == rid).first()
    if points:
        errmsg.append("Points entry already exists for given user at this restaurant.")

    if not errmsg:
        points = Points(uid = uid, rid = rid, points = 0)
        db.session.add(points)
        db.session.commit()
        return None
    return errmsg


def get_points(uid, rid):
    """
    Fetches a row from the Points table.

    Retrieves a row pertaining the given user ID and restaurant ID from the Points table
    in the database.

    Args:
        uid: The user ID pertaining to the user whose points information is being 
          retrieved. An integer.
        rid: The restaurant ID pertaining to the restaurant whose points information 
          is being retrieved. An integer.
    Returns:
        A points entry with matching user ID and restaurant ID as the ones provided,
        None otherwise.
    """
    points = Points.query.filter(Points.uid == uid).filter(Points.rid == rid).first()
    return points


def update_points(uid, rid, increment):
    """
    Updates the points value of a row from the Points table.

    Args:
        uid: The user ID pertaining to the user whose points information is being 
          updated. An integer.
        rid: The restaurant ID pertaining to the restaurant whose points information 
          is being updated. An integer.
        increment: The amount of points by which the points entry's current point value
          should be incremented. An integer.
    Returns:
        None if the points entry was successfully updated, a list of
        error messages otherwise.
    """
    errmsg = []

    points = Points.query.filter(Points.uid == uid).filter(Points.rid == rid).first()
    if not points:
        errmsg.append("Points entry does not exist for the given user ID and restaurant ID.")
    elif (points.points + increment) < 0:
        errmsg.append("A points entry cannot have a negative point count.")

    if not errmsg:
        Points.query.filter(Points.uid == uid).filter(Points.rid == rid).update(dict(points=points.points + increment))
        db.session.commit()
        return None

    return errmsg