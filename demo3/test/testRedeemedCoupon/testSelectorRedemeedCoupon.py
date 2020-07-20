import unittest
from models import User, Coupon, Restaurant, Employee, Customer_Coupons
from models import db
import time
from datetime import datetime
from app import app
from helpers import coupon as chelper

BEGIN = datetime.strptime("1 May, 2020", "%d %B, %Y")
END = datetime.strptime("30 June, 2020", "%d %B, %Y")


class SelectCustomerCoupons(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_no_coupon(self):
        customer_coupon_list = chelper.get_customer_coupons_by_rid(20)
        self.assertEqual(customer_coupon_list, [])
        return None


    def test_one_coupon(self):
        restaurant = Restaurant(name = "David's Restaurant", address = "1234 Main Street", uid = 17)
        db.session.add(restaurant)
        db.session.commit()
        coupon = Coupon(rid = restaurant.rid, name="test", points=10, description="50% off", begin=BEGIN, expiration=END)
        user = User(uid = 5, name = "Joe", email = "joe@gmail.com", password = "password", type = -1)
        db.session.add(coupon)
        db.session.commit()
        db.session.add(user)
        db.session.commit()
        customer_coupon = Customer_Coupons(cid = coupon.cid, rid = restaurant.rid, uid = user.uid, amount = 1)
        db.session.add(customer_coupon)
        db.session.commit()

        customer_coupon_list = chelper.get_customer_coupons_by_rid(restaurant.rid)

        self.assertEqual(customer_coupon_list,[
            {
                "email": "joe@gmail.com",
                "cname": "test",
                "begin": BEGIN,
                "expiration": END,
                "description": "50% off",
                "points": 10
            }
        ])
        

    def test_many_coupon(self):
                restaurant = Restaurant(name = "David's Restaurant", address = "1234 Main Street", uid = 17)
                db.session.add(restaurant)
                db.session.commit()
                coupon = Coupon(rid = restaurant.rid, name="test", points=10, description="50% off", begin=BEGIN, expiration=END)
                user = User(uid = 5, name = "Joe", email = "joe@gmail.com", password = "password", type = -1)
                db.session.add(coupon)
                db.session.commit()
                db.session.add(user)
                db.session.commit()
                customer_coupon = Customer_Coupons(cid = coupon.cid, rid = restaurant.rid, uid = user.uid, amount = 3)
                db.session.add(customer_coupon)
                db.session.commit()

                customer_coupon_list = chelper.get_customer_coupons_by_rid(restaurant.rid)

                self.assertEqual(customer_coupon_list,[
                    {
                        "email": "joe@gmail.com",
                        "cname": "test",
                        "begin": BEGIN,
                        "expiration": END,
                        "description": "50% off",
                        "points": 10
                    },
                    {
                        "email": "joe@gmail.com",
                        "cname": "test",
                        "begin": BEGIN,
                        "expiration": END,
                        "description": "50% off",
                        "points": 10
                    },
                    {
                        "email": "joe@gmail.com",
                        "cname": "test",
                        "begin": BEGIN,
                        "expiration": END,
                        "description": "50% off",
                        "points": 10
                    }
                ])
