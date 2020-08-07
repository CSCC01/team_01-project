from models import Experience
from databaseHelpers.user import *

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

def get_data(list):
    data_list = []
    rank = 1
    for l in list:
        data={"username": get_user_name_by_uid(l[0]),
              "exp": l[1],
              "rank": rank}
        rank+=1
        data_list.append(data)
    return data_list

