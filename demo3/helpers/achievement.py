from models import Achievements
from exts import db

"""
Inserts a valid achievement into the database

Returns error messages if insertion failed, none otherwise
"""
def insert_achievement(rid, name, experience, points, type, item, amount):
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
            achievement = Achievements(rid = rid, name = name, experience = experience, points = points, type = 1, value = value)
        # Example: Buy item amount times
        else:
            item.replace(";", "")
            value = item + ";" + str(amount)
            achievement = Achievements(rid = rid, name = name, experience = experience, points = points, type = 0, value = value)
        db.session.add(achievement)
        db.session.commit()

    return errmsg
