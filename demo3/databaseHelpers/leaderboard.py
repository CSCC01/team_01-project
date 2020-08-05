from models import Experience

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


def top_n_in_order(rid,n):
    """
    :param rid: restaurant id
    :param n:  top n, an integer, default 50
    :return: a sorted list of tuples of length n, for example
    [(5, 170), (32, 158), (1, 66), (10, 64), (18, 58)]
    sorted exp -> result[x][1]
    corresponding uid -> result[x][0]
    """
    dict = {}
    exp = Experience.query.filter(Experience.rid==rid).all()
    for e in exp:
        dict[e.uid] = e.experience
    sort_list = sorted(dict.items(), key=lambda item:item[1], reverse=True)
    return sort_list[:n]

def get_rank(uid, rid):
    """
    :param uid:
    :param rid:
    :return:
    """
    # TODO get customer rank at current restaurant
