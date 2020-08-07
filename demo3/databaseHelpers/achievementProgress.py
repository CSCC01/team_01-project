from models import Achievements, Customer_Achievement_Progress, Points, Experience

from databaseHelpers.achievement import *
from databaseHelpers.experience import *
from databaseHelpers.points import *
from databaseHelpers.restaurant import get_restaurant_name_by_rid
from datetime import datetime

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db

NOT_STARTED = 0
IN_PROGRESS = 1
COMPLETE = 2

def get_achievement_progress_by_uid(uid):
    """
    Fetches rows from the Achievement Progress table.

    Retrieves a list of achievement progress from the Achievement Progress table that
    belongs to the user with the given user ID.

    Args:
        uid: A user ID that corresponds to a user in the User
          table. An integer.

    Returns:
        A list of achievement progress for a user with user ID that
        matches uid.
    """
    achievement_progress_list = []
    achievement_progress = Customer_Achievement_Progress.query.filter(Customer_Achievement_Progress.uid == uid).all()
    for a in achievement_progress:
        dict = {
            "aid": a.aid,
            "uid": a.uid,
            "progress": a.progress,
            "progressMax": a.total,
            "update": a.update
        }
        achievement_progress_list.append(dict)
    return achievement_progress_list

def get_achievement_with_progress_data(aid, uid):
    """
    Appends progress data for a given user and a fiven achievement

    Args:
        aid: An achievement ID that corresponds to an achievement in the
            Achievement table. An integer.
        uid: A user ID that corresponds to a user in the User
            table. An integer.

    Returns:
        An achievement with progress data.
    """
    achievement = get_achievement_by_aid(aid)
    progress = get_exact_achivement_progress(aid, uid)

    if (achievement == 'Not Found'):
        return None
    if (progress == 'Not Found'):
        progressCount = 0
    else:
        progressCount = progress.progress

    dict = {
        "aid": achievement.aid,
        "name": achievement.name,
        "description": get_achievement_description(achievement),
        "experience": achievement.experience,
        "points": achievement.points,
        "progressMax": get_achievement_progress_maximum(achievement),
        "progress": progressCount
    }
    return dict

def get_achievements_with_progress_data(achievements, uid):
    """
    Appends progress data for a given user to each achievement at a given
    restaurant.

    Args:
        achievements: The achievements from a given restaurant. A list of dict
            items with aid, description, experience, points, and progressMax keys.
        uid: A user ID that corresponds to a user in the User
            table. An integer.

    Returns:
        A list of achievements with progress data.
    """
    achievement_progress_list = get_achievement_progress_by_uid(uid)
    filtered_achievements = []
    for a in achievements:
        has_progress = False
        for p in achievement_progress_list:
            if a["aid"] == p["aid"]:
                if p["progress"] == p["progressMax"]:
                    a["status"] = COMPLETE
                else:
                    a["status"] = IN_PROGRESS
                a["progress"] = p["progress"]
                has_progress = True
                achievement_progress_list.remove(p)
                break
        if not has_progress:
            a["progress"] = 0
            a["status"] = NOT_STARTED
        filtered_achievements.append(a)
    return filtered_achievements

def get_recently_started_achievements(achievements, uid):
    """
    Finds the 3 most recently started incomplete achievements for a user
    at a restaurant and appends the user's progress data to each achievement.

    Args:
        achievements: The achievements from a given restaurant. A list of dict
            items with aid, description, experience, points, and progressMax keys.
        uid: A user ID that corresponds to a user in the User
            table. An integer.

    Returns:
        A list of 3 or less achievements with progress data.
    """
    achievement_progress_list = get_achievement_progress_by_uid(uid)
    achievement_progress_list.reverse()

    recent_achievements = []

    for p in achievement_progress_list:
        for a in achievements:
            if a["aid"] == p["aid"]:
                if p["progress"] < p["progressMax"]:
                    a["status"] = IN_PROGRESS
                    a["progress"] = p["progress"]
                    recent_achievements.append(a)
                achievements.remove(a)
                break
        if len(recent_achievements) == 3:
            break
    
    return recent_achievements

def get_exact_achivement_progress(aid, uid):
    """
    Get the exact achivement progress by applying both aid and uid to it
    :param aid: achievement id
    :param uid: user id
    :return: Customer_Achievement_Progress if found
             'Not Found' if not found
    """
    achievement_progress = Customer_Achievement_Progress.query.filter(Customer_Achievement_Progress.aid==aid,
                                                                      Customer_Achievement_Progress.uid==uid).first()

    if achievement_progress:
        return achievement_progress
    else:
        return 'Not Found'

def get_progress_completion_status(achievements_progress):
    """
    Checks whether a progress entry is complete.

    Args:
        achievements_progress: The progress entry to check

    Returns:
        The progress completion status.
    """
    if achievements_progress == 'Not Found':
        return NOT_STARTED
    elif achievements_progress.progress == achievements_progress.total:
        return COMPLETE
    return IN_PROGRESS


def add_one_progress_bar(achievements_progress, aid, uid):
    ach = get_achievement_by_aid(aid)
    total = get_achievement_progress_maximum(ach)
    if achievements_progress == 'Not Found':
        achievements_progress = insert_new_achievement(aid, uid, total)

    achievements_progress.progress += 1
    achievements_progress.update = datetime.now()
    if achievements_progress.progress == achievements_progress.total:
        complete_progress(achievements_progress)
    db.session.commit()
    return None


def complete_progress(achievement_progress):
    rid = get_rid_points_exp_by_aid(achievement_progress.aid)['rid']
    uid = achievement_progress.uid
    points = get_rid_points_exp_by_aid(achievement_progress.aid)['points']
    exp = get_rid_points_exp_by_aid(achievement_progress.aid)['exp']

    user_point = get_points(uid, rid)
    if not user_point:
        insert_points(uid, rid)
    update_points(uid, rid, points)

    user_exp = get_experience(uid, rid)
    if not user_exp:
        insert_experience(uid, rid)
    update_experience(uid, rid, exp)
    db.session.commit()
    return None


def get_rid_points_exp_by_aid(aid):
    achievement = Achievements.query.filter(Achievements.aid==aid).first()
    if achievement:
        return {'rid': achievement.rid,
                'points': achievement.points,
                'exp': achievement.experience}
    return 'Not Found'

def insert_new_achievement(aid,uid,total):
    update = datetime.now()
    ap = Customer_Achievement_Progress(aid=aid, uid=uid, progress=0, total=total, update=update)
    db.session.add(ap)
    db.session.commit()
    return ap

# def get_no_complete_achievement_progress_by_uid(uid):
#     """
#     Fetches rows from the Achievement Progress table.
#
#     Retrieves a list of achievement progress from the Achievement Progress table that
#     belongs to the user with the given user ID.
#
#     Args:
#         uid: A user ID that corresponds to a user in the User
#           table. An integer.
#
#     Returns:
#         A list of achievement progress for a user with user ID that
#         matches uid.
#     """
#     achievement_progress_list = []
#     achievement_progress = Customer_Achievement_Progress.query.filter(Customer_Achievement_Progress.uid == uid,
#                                 Customer_Achievement_Progress.progress < Customer_Achievement_Progress.total).all()
#     for a in achievement_progress:
#         dict = {
#             "aid": a.aid,
#             "uid": a.uid,
#             "progress": a.progress,
#             "progressMax": a.total,
#             "update": a.update
#         }
#         achievement_progress_list.append(dict)
#     return achievement_progress_list


def get_recently_update_achievements(uid):
    """

    :param uid: user id
    :return: a list of recent achievement progress (<=3)
    """
    from operator import itemgetter
    recent_achievements = []
    ap_list = get_achievement_progress_by_uid(uid)
    new_list = sorted(ap_list, key=itemgetter('update'), reverse=True)
    for ap in new_list[:3]:
        recent_achievements.append(get_exact_achivement_progress(ap['aid'], ap['uid']))
    return recent_achievements

def get_updated_info(recent_achievements):
    """
    :param recent_achievements: a list of achievement_progress (<=3) sorted by updated time
    :return: a dict of these achievement_progress containing following info:
    'aid', 'uid', 'progress', 'progressMax', 'description', 'name', 'points' and 'experience'
    """
    achievements = []
    for ap in recent_achievements:
        a = Achievements.query.filter(Achievements.aid == ap.aid).first()
        achievement = {'aid': ap.aid,
                       'uid': ap.uid,
                       'progress': ap.progress,
                       'progressMax': ap.total,
                       'description': get_achievement_description(a),
                       'name': a.name,
                       'points': a.points,
                       'experience': a.experience,
                       'rname': get_restaurant_name_by_rid(a.rid),
                       'raddress': get_restaurant_address(a.rid)
                       }
        achievements.append(achievement)
    return achievements



