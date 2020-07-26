from models import Achievement, Customer_Achievement_Progress

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


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

def get_achievements_with_no_progress(achievements, uid):
    """
    Filters achievements with zero progress by the given user from a 
    list of achievements and appends progress data to each achievement.

    Args:
        achievements: The achievements to be filtered. A list of dict items
            with aid, description, experience, points, and progressMax keys.
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
                has_progress = True
                break
        if not has_progress:
            a["progress"] = 0
            filtered_achievements.append(a)
    return filtered_achievements



