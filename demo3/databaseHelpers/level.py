from models import Experience

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


def convert_experience_to_level(experience):
    """
    Calculates user level based on the user's total experience at a given restaurant.

    A user requires 100 experience to level up from level 0 to level 1, 200 experience to
    level up from level 1 to level 2, 300 experience to level up from level 2 to level
    3, etc. Therefore a level 0 user has 0-99 experience, a level 1 user has 100-299
    experience, a level 2 user has 300-599 experience, etc.

    Args:
        experience: The number of experience a user currently has. An integer.

    Returns:
        The integer level of the user based on the given experience.
    """
    level = 0
    p = experience / 100.0
    
    while (level + 1) <= p:
      level = level + 1
      p = p - level

    return level

def get_experience_since_last_level(level, experience):
    """
    Calculates the number of experience earned by a user at a restaurant since the user's 
    last level up.

    Args:
        level: The current level of the user. An integer.
        experience: The total experience of the user. An integer.

    Returns:
        The integer number of experience earned since the user's last level up.
    """
    return experience - (sum(range(level+1))*100)