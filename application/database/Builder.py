from database.Helper import *

def buildUser(attributes):
    query = "SELECT * FROM user WHERE email = :email AND password = :password"

    # Creates a user object and pulls all attributes from the database
    user = select_one(query, attributes)
    return user

def insertUser(attributes):
    query = "INSERT INTO user (tid, name, email, password, address) VALUES (:tid, :name, :email, :password, :address)"
    insert(query, attributes)


def getUserByEmail(attributes):
    query = "SELECT * FROM user WHERE email = :email"
    user = select_one(query, attributes)
    return user


def getResturantByName(attributes):
    query = "SELECT * FROM restaurant WHERE rname = :rname"
    resturant = select_one(query, attributes)
    return resturant

def insertResturant(attributes):
    query = "INSERT INTO restaurant (rname, uid) VALUES (:rname, :uid)"
    insert(query, attributes)

def getCouponsById(attributes):
    query = "SELECT * FROM coupons, restaurant WHERE coupons.rid = restaurant.rid and restaurant.uid = :uid"
    coupon = select_all(query, attributes)
    return coupon

def insertCoupon(attributes):
    query = "INSERT INTO coupons (rid, name, amount, description, expiration) VALUES (:rid, :name, :amount, :description, :expiration)"
    insert(query, attributes)

def getRid(attributes):
    query = "SELECT * FROM restaurant WHERE uid = :uid"
    restaurant = select_one(query, attributes)
    return restaurant
