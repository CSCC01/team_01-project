from models import Achievements
import datetime
from datetime import date

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db

def get_achievements_by_rid(rid):
    """
    Fetches rows from the Achievement table.

    Retrieves a list of achievements from the Achievement table that belong to the
    restaurant with the given restaurant ID.

    Args:
        rid: A restaurant ID that corresponds to a restaurant in the Restaurant
          table. A integer.

    Returns:
        A list of achievements for a restaurant with restaurant ID that
        matches rid.
    """
    achievement_list = []
    achievements = Achievements.query.filter(Achievements.rid == rid).all()
    for a in achievements:
        dict = {
            "aid": a.aid,
            "name": a.name,
            "description": get_achievement_description(a),
            "experience": a.experience,
            "points": a.points,
            "progressMax": get_achievement_progress_maximum(a),
            "expired": is_today_in_achievement_date_range(a)
        }
        achievement_list.append(dict)
    return achievement_list

def get_achievement_description(achievement):
    """
    Generates an achievement description based on the achievement type
    and values.

    Args:
        achievement: The achievement whose description is to be generated.
                     Achievement values must be in the form "ITEM;QUANTITY".

    Returns:
        A description for the given achievement.
    """
    values = get_achievement_data(achievement)
    switcher = {
        0: "Buy " + values[0] + " " + values[1] + " times",
        1: "Spend $" + values[1] + " in a single visit",
        2: "Visit with a group of at least " + values[1] + " people",
        3: "Visit " + values[1] + " times"
    }

    description = switcher.get(achievement.type)
    if (values[2] == "False"):
        description = description + " between " + values[3] + " and " + values[4] + "."
    else:
        description = description + "."

    return description


def get_achievement_progress_maximum(achievement):
    """
    Calculates a progress maximum for an achievement based on the achievement type
    and values.

    E.g. the progress maximum is x for an achievement whose progress is tracked as
    "? out of x complete".

    Args:
        achievement: The achievement whose progress maximum is to be calculated
                     Achievement values must be in the form "ITEM;QUANTITY".
                     Quantity must be an integer for type 0 achievements.

    Returns:
        A progress maximum for a given achievement.
    """
    values = get_achievement_data(achievement)
    switcher = {
        0: values[1],
        1: 1,
        2: 1,
        3: values[1]
    }
    return int(switcher.get(achievement.type))

def is_today_in_achievement_date_range(achievement):
    """
    Checks whether today is in, before, or after the range of
    valid dates for an achievement.

    Args:
        achievement: The achievement to be checked

    Returns:
        -1, if today is before the achievement date range;
        0, if today is within the achievement date range;
        1, if today is after the achievement date range.
    """
    today = date.today()
    values = get_achievement_data(achievement)
    if values[2] == "False":
        e = (values[4]).split('-')
        expiration = datetime.date(int(e[0]), int(e[1]), int(e[2]))
        if today > expiration:
            return 1

        e = (values[3]).split('-')
        start = datetime.date(int(e[0]), int(e[1]), int(e[2]))
        if today < start:
            return -1
    return 0

def get_achievement_data(achievement):
    """
    Splits achievement value into a data list.

    Args:
        achievement: The achievement whose value data is to be processed

    Returns:
        A data list for a given achievement.
    """
    return achievement.value.split(';')


def get_errmsg(name, experience, points, type, value):
    """
    Gets all error messages that can occur from inserting a achievement.
    Args:
        rid: A restuarants ID. Integer value.
        name: The name of a restaurant. String value.
        experience: The reward experience value. Integer value.
        points: The reward points value. Integer value
        type: The type of achievement:
          0: buy item amount times.
          1: Spend $$.$$ amount.
          2: Visit with a group.
          3: Visit a specific amount of time.
          Interger value.
        value: of the form: "INT;STRING;BOOLEAN;DATE;DATE"
    """
    errmsg = []

    if name == "":
        errmsg.append("Invalid achievement name, please provide an achievement name.")
    if (experience == "" and points == "") or (experience == '0' and points == '0'):
        errmsg.append("Missing experience and points, please provide at least one reward.")
    if experience != "" and int(experience) < 0:
        errmsg.append("Invalid experience, please provide non-negative value.")
    if points != "" and int(points) < 0:
        errmsg.append("Invalid points, please provide non-negative value.")

    data = value.split(';')

    if type == 0 and data[0] == "":
        errmsg.append("Missing an item, please provide an item for the achievement.")
    if data[1] == "" or float(data[1]) < 0:
        errmsg.append("Invalid amount, please provide a positive value.")
    if data[2] == "False" and (data[3] == "" or data[4] == ""):
        errmsg.append("Missing start or expiration date.")
    if data[2] == "False" and data[4] != "":
        today = date.today()
        e = (data[4]).split('-')
        expiration = datetime.date(int(e[0]), int(e[1]), int(e[2]))
        if expiration < today:
            errmsg.append("This achievemnt is already outdated.")
        
        if data[3] != "":
            b = (data[3]).split('-')
            begin = datetime.date(int(b[0]), int(b[1]), int(b[2]))
            if expiration < begin:
                errmsg.append("Invalid date interval, begin date must be before expiration date.")

    return errmsg


def insert_achievement(rid, name, experience, points, type, value):
    """
    Gets all error messages that can occur from inserting a achievement.

    Args:
        rid: A restuarants ID. Integer value.
        name: The name of a restaurant. String value.
        experience: The reward experience value. Integer value.
        points: The reward points value. Integer value
        type: The type of achievement:
          0: buy item amount times.
          1: Spend $$.$$ amount.
          2: Visit with a group.
          3: Visit a specific amount of time.
          Interger value.
        value: of the form: "INT;STRING;BOOLEAN;DATE;DATE"
    """

    achievement = Achievements(rid = rid, name = name, experience = experience, points = points, type = type, value = value)
    db.session.add(achievement)
    db.session.commit()


def filter_expired_achievements(rid):
    """
    Filters out rows from the achievemnt table.

    Filters out achievements that are past their expiration date.

    Args:
        rid: A restuarants ID that corresponds to a restaurant in the restaurant
          table. Integer value.

    Returns: None
    """
    today = date.today()
    achievements = Achievements.query.filter(Achievements.rid == rid).all()
    achievement_list = []

    for a in achievements:
        dict = {
            "aid": a.aid,
            "name": a.name,
            "description": get_achievement_description(a),
            "experience": a.experience,
            "points": a.points,
            "progressMax": get_achievement_progress_maximum(a)
        }
        values = a.value.split(';')
        if values[2] == "False":
            e = (values[4]).split('-')
            expiration = datetime.date(int(e[0]), int(e[1]), int(e[2]))
            if today <= expiration:
                achievement_list.append(dict)
        else:
            achievement_list.append(dict)
    return achievement_list


def delete_achievement(aid):
    """
    Removes a row from the Achievement table.

    Deletes an achievement from the database.

    Args:
        aid: An achievement ID that corresponds to a achievement in the Achievement table.
        An integer.

    Returns:
        (if deleted) None.
        (if not) "No such achievement"
    """
    achievement = Achievements.query.filter(Achievements.aid == aid).first()
    if achievement:
        db.session.delete(achievement)
        db.session.commit()
        return None
    return "No such achievement"

def get_achievement_by_aid(aid):
    ach = Achievements.query.filter(Achievements.aid == aid).first()
    if ach:
        return ach
    return "Not Found"
