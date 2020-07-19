from models import Points
from exts import db


def convert_points_to_level(points):
    """
    Calculates user level based on the user's total points at a given restaurant.

    A user requires 100 points to level up from level 0 to level 1, 200 points to
    level up from level 1 to level 2, 300 points to level up from level 2 to level
    3, etc. Therefore a level 0 user has 0-99 points, a level 1 user has 100-299
    points, a level 2 user has 300-599 points, etc.

    Args:
        points: The number of points a user currently has. An integer.

    Returns:
        The integer level of the user based on the given points.
    """
    level = 0
    p = points / 100.0
    
    while (level + 1) <= p:
      level = level + 1
      p = p - level

    return level

def get_points_since_last_level(level, points):
    """
    Calculates the number of points earned by a user at a restaurant since the user's 
    last level up.

    Args:
        level: The current level of the user. An integer.
        points: The total points of the user. An integer.

    Returns:
        The integer number of points earned since the user's last level up.
    """
    return points - (sum(range(level+1))*100)