from models import Achievements

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
        0: "Buy " + values[0] + " " + values[1] + " times.",
        1: "Spend $" + values[1] + " in a single visit."
    }
    return switcher.get(achievement.type)

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
        1: 1
    }
    return int(switcher.get(achievement.type))

def get_achievement_data(achievement):
    """
    Splits achievement value into a data list.

    Args:
        achievement: The achievement whose value data is to be processed

    Returns:
        A data list for a given achievement.
    """
    return achievement.value.split(';')


def insert_achievement(rid, name, experience, points, type, item, amount):
    """
    Inserts a a row into the Acheievments table.

    Args:
        rid: A restuarants ID. Integer value.
        name: The name of a restaurant. String value.
        experience: The reward experience value. Integer value.
        points: The reward points value. Integer value
        type: The type of achievement:
          '0': buy item amount times.
          '1': Spend $amount.
          String value.
        item: The item the required for type 0. String value
        amount: The amount of money/items needed to complete acheievement. Integer value.

    Returns:
        A list of error messages from inserting an object, if no errors occured, returns an empty list.
    """
    errmsg = []

    if name == "":
        errmsg.append("Invalid achievement name, please provide an achievement name.")
    if experience == "" and points == "":
        errmsg.append("Missing experience and points, please at least provide experience or points.")
    if experience != "" and int(experience) < 0:
        errmsg.append("Invalid experience, please provide non-negative value.")
    if points != "" and int(points) < 0:
        errmsg.append("Invalid points, please provide non-negative value.")
    if type == "0" and item == "":
        errmsg.append("Missing an item, please provide an item for the achievement.")
    if amount == "":
        errmsg.append("Missing an amount, please provide an amount for the achievement.")

    if not errmsg:
        # Example: Spend $xx.xx in a single visit
        if type == "1":
            value = ";" + str(amount)
            achievement = Achievements(rid = rid, name = name, experience = experience, points = points, type = 1, value= value)
        # Example: Buy item amount times
        else:
            item = item.replace(";", "")
            value = item + ";" + str(amount)
            achievement = Achievements(rid = rid, name = name, experience = experience, points = points, type = 0, value = value)
        db.session.add(achievement)
        db.session.commit()

    return errmsg

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

