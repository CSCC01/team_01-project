from models import Thresholds, Experience
from sqlalchemy import asc, desc
from databaseHelpers.level import *
from databaseHelpers.points import *

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db

def insert_threshold(rid, level, reward):
    """
    Insert the threshold to the database for the restaurant given.

    Args:
        rid: The unique ID of the restaurant. An integer.
        level: The required level to reach the milestone and get rewards
        reward: The amount of experience added if level reached

    Returns:
        None if threshold was successfully added to the Thresholds table,
        a list of error messages otherwise.
    """
    errmsg = []
    if level == "":
        errmsg.append("Invalid level requirment.")
    if level != "" and int(level) < 0:
        errmsg.append("Invalid level requirment, please provide non-negative value.")
    if reward == "":
        errmsg.append("Invalid amount for points.")
    if reward != "" and int(reward) < 0:
        errmsg.append("Invalid points, please provide non-negative value.")
    if not errmsg:
        threshold = Thresholds(rid = rid, level = level, reward = reward)
        db.session.add(threshold)
        db.session.commit()

    return errmsg


def delete_threshold(rid, level):
    """
    Delete the threshold from the database

    Args:
        rid: The unique ID of the restaurant. An integer.
        level: The required level to reach the milestone and get rewards

    Returns:
        None
    """
    threshold = Thresholds.query.filter(Thresholds.rid == rid, Thresholds.level == level).first()
    if threshold:
        db.session.delete(threshold)
        db.session.commit()


def get_thresholds(rid):
    """
    Get a list of dictionary containing rid, level and reward form the restaurant of given rid

    Args:
        rid: The unique ID of the restaurant. An integer.

    Returns:
        a list of dictionary of key "rid", "level" and "reward"
    """
    thresholds = Thresholds.query.filter(Thresholds.rid == rid).order_by(Thresholds.level.asc()).all()
    threshold_list = []
    for t in thresholds:
        dict = {
            "rid": t.rid,
            "level": t.level,
            "reward": t.reward
        }
        threshold_list.append(dict)
    return threshold_list


def update_threshold(rid, level, reward):
    """
    Update the threshold in the database for the restaurant given.

    Args:
        rid: The unique ID of the restaurant. An integer.
        level: The required level to reach the milestone and get rewards
        reward: The amount of experience added if level reached

    Returns:
        None if threshold was successfully updated in the Thresholds table,
        a list of error messages otherwise.
    """
    errmsg = []
    threshold = Thresholds.query.filter(Thresholds.rid == rid, Thresholds.level == level).first()

    if level == "":
        errmsg.append("Invalid level requirment.")
    if level != "" and int(level) < 0:
        errmsg.append("Invalid level requirment, please provide non-negative value.")
    if reward == "":
        errmsg.append("Invalid amount for points.")
    if reward != "" and int(reward) < 0:
        errmsg.append("Invalid points, please provide non-negative value.")
    if not errmsg and threshold:
        threshold.reward = reward
        db.session.commit()

    return errmsg


def check_threshold(rid, level):
    """
    Check if threshold exist.

    Args:
        rid: The unique ID of the restaurant. An integer.
        level: The required level to reach the milestone and get rewards

    Returns:
        True if threshold exists
        False if threshold doesn't exist
    """
    threshold = Thresholds.query.filter(Thresholds.rid == rid, Thresholds.level == level).first()
    return threshold != None


def get_milestone(uid, rid):
    """
    Get a list of dictionary of the milestone.

    Args:
        uid: he unique ID of the user. An integer.
        rid: The unique ID of the restaurant. An integer.

    Returns:
        A list of dictionary containing level and reward of thr certain restaurant
        None if experience doesn't exist
    """
    experience = Experience.query.filter(Experience.uid == uid).filter(Experience.rid == rid).first()
    if experience:
        experience = experience.experience
        level = convert_experience_to_level(experience)
        threshold = Thresholds.query.filter(Thresholds.rid == rid, Thresholds.level > level).order_by(asc(Thresholds.level)).first()
        if threshold:
            return {
                "level": threshold.level,
                "reward": threshold.reward
            }
    return None

def get_incomplete_milestones(rid, level):
    """
    Get all the milestone that is not completed in certain restaurant.

    Args:
        rid: The unique ID of the restaurant. An integer.
        level: The required level to reach the milestone and get rewards

    Returns:
        A list of all incomplete milestone.
    """
    threshold_list = get_thresholds(rid)
    incomplete_list = []
    for t in threshold_list:
        if t["level"] > level:
            incomplete_list.append(t)

    return incomplete_list
