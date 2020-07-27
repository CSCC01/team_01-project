from models import Achievement

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
    achievements = Achievement.query.filter(Achievement.rid == rid).all()
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
