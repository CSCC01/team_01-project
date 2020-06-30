import sqlite3

DATABASE = 'database/pickeasy.db'

# Formats a dictinary from one row (the first) from the database
def get_one(cursor, row):
    d = {}
    if (len(row) > 0):
        for i in range(len(row[0])):
            d[cursor.description[i][0]] = row[0][i]

    return d


# Formats a list of dictinaries for all rows given
def get_all(cursor, row):
    l = []

    for i in range(len(row)):
        d = {}
        for j in range(len(row[i])):
            d[cursor.description[j][0]] = row[i][j]
        l.append(d)

    return l

def select_one(query, attributes):
    conn = sqlite3.connect(DATABASE);
    c = conn.cursor()
    c.execute(query, attributes)
    result = c.fetchall()
    dict = get_one(c, result)
    conn.commit()
    conn.close()

    return dict


def select_all(query, attributes):
    conn = sqlite3.connect(DATABASE);
    c = conn.cursor()
    c.execute(query, attributes)
    result = c.fetchall()
    dict = get_all(c, result)
    conn.commit()
    conn.close()

    return dict

def insert(query, attributes):
    conn = sqlite3.connect(DATABASE);
    c = conn.cursor()
    c.execute(query, attributes)
    conn.commit()
    conn.close()
