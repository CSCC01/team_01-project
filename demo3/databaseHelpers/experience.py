from models import Experience

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


def insert_experience(uid, rid):
    """
    Inserts a 0 experience entry into experience table for a given user and restaurant.

    Args:
        uid: A user ID that corresponds to a user in the User
          table. A integer.
        rid: A restaurant ID that corresponds to a restaurant in the Restaurant
          table. A integer.

    Returns:
        experience if entry was successfully added to the experience table, a list of
        error messages otherwise.
    """
    errmsg = []

    experience = Experience.query.filter(Experience.uid == uid).filter(Experience.rid == rid).first()
    if experience:
        errmsg.append("Experience entry already exists for given user at this restaurant.")

    if not errmsg:
        experience = Experience(uid = uid, rid = rid, experience = 0)
        db.session.add(experience)
        db.session.commit()
        return None
    return errmsg


def get_experience(uid, rid):
    """
    Fetches a row from the experience table.

    Retrieves a row pertaining the given user ID and restaurant ID from the experience table
    in the database.

    Args:
        uid: The user ID pertaining to the user whose experience information is being 
          retrieved. An integer.
        rid: The restaurant ID pertaining to the restaurant whose experience information 
          is being retrieved. An integer.
    Returns:
        A experience entry with matching user ID and restaurant ID as the ones provided,
        None otherwise.
    """
    experience = Experience.query.filter(Experience.uid == uid).filter(Experience.rid == rid).first()
    return experience


def update_experience(uid, rid, increment):
    """
    Updates the experience value of a row from the experience table.

    Args:
        uid: The user ID pertaining to the user whose experience information is being 
          updated. An integer.
        rid: The restaurant ID pertaining to the restaurant whose experience information 
          is being updated. An integer.
        increment: The amount of experience by which the experience entry's current point value
          should be incremented. An integer.
    Returns:
        None if the experience entry was successfully updated, a list of
        error messages otherwise.
    """
    errmsg = []

    experience = Experience.query.filter(Experience.uid == uid).filter(Experience.rid == rid).first()
    if not experience:
        errmsg.append("Experience entry does not exist for the given user ID and restaurant ID.")
    elif increment < 0:
        errmsg.append("Experience cannot be incremented by a negative number.")

    if not errmsg:
        Experience.query.filter(Experience.uid == uid).filter(Experience.rid == rid).update(dict(experience=experience.experience + increment))
        db.session.commit()
        return None

    return errmsg