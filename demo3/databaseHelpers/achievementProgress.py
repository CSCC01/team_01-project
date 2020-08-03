from models import Achievements, Customer_Achievement_Progress

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
            "progress": a.progress,
            "progressMax": a.total,
        }
        achievement_progress_list.append(dict)
    return achievement_progress_list

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