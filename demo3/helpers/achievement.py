from models import Achievement
from exts import db

"""
Inserts a valid achievement into the database

Returns error messages if insertion failed, none otherwise
"""
def insert_achievement(rid, name, description, experience, points, requireItem, requireFee, item):
    errmsg = []

    if name == "":
        errmsg.append("Invalid achievement name, please provide an achieve name.")
    if description == "":
        errmsg.append("Invalid description of achievement, please provide a description.")
    if experience == "" and points == "":
        errmsg.append("Missing experience and points, please at least provide experience or points.")
    if int(experience) < 0:
        errmsg.append("Invalid experience, please provide non-negative value.")
    if int(points) < 0:
        errmsg.append("Invalid points, please provide non-negative value.")
    if int(experience) < 0 and int(points) < 0:
       errmsg.append("Invalid experience and points, please provide non-negative value.")
    if item:
        if requireItem == "":
            errmsg.append("Missing Item.")
        if int(requireItem) < 0:
            errmsg.append("Invalid requirement, please provide non-negative value.")
    else:
        if requireFee == "":
            errmsg.append("Missing Fee.")
        if float(requireFee) < 0.0: 
            errmsg.append("Invalid requirement, please provide non-negative value.")
    
    if not errmsg:
        if item:
            achievement = Achievement(rid = rid, name = name, description = description, experience = experience, points = points, requireItem = requireItem)
        else:
            achievement = Achievement(rid = rid, name = name, description = description, experience = experience, points = points, requireFee = requireFee)
        db.session.add(achievement)
        db.session.commit()
        return None
    else:
        return errmsg