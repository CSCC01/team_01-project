import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from datetime import datetime
from app import app
from helpers import coupon as couponhelper

BEGIN = datetime.strptime("1 May, 2020", "%d %B, %Y")
END = datetime.strptime("30 June, 2020", "%d %B, %Y")


class SelectCouponTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_coupon_single(self):
        coupon = Coupon(rid=12, name="test", points=10, description="1$ off", begin=BEGIN, expiration=END)
        db.session.add(coupon)
        db.session.commit()
        coupon_list = couponhelper.get_coupons(12)
        self.assertEqual(coupon_list,[{'begin': BEGIN,
                     'cid': 1,
                     'description': '1$ off',
                     'expiration': END,
                     'name': 'test',
                     'points': 10}])

    def test_coupon_multi(self):
        coupon1 = Coupon(rid=12, name="test1", points=10, description="1$ off", begin=BEGIN, expiration=END)
        coupon2 = Coupon(rid=12, name="test2", points=20, description="2$ off", begin=BEGIN, expiration=END)
        coupon3 = Coupon(rid=12, name="test3", points=30, description="3$ off", begin=BEGIN, expiration=END)
        db.session.add(coupon1)
        db.session.add(coupon2)
        db.session.add(coupon3)
        db.session.commit()
        coupon_list = couponhelper.get_coupons(12)
        self.assertEqual(coupon_list, [{'begin': BEGIN,
                     'cid': 1,
                     'description': '1$ off',
                     'expiration': END,
                     'name': 'test1',
                     'points': 10},
                    {'begin': BEGIN,
                     'cid': 2,
                     'description': '2$ off',
                     'expiration': END,
                     'name': 'test2',
                     'points': 20},
                    {'begin': BEGIN,
                     'cid': 3,
                     'description': '3$ off',
                     'expiration': END,
                     'name': 'test3',
                     'points': 30}])

    def test_coupon_none(self):
        coupon1 = Coupon(rid=12, name="test1", points=10, description="1$ off", begin=BEGIN, expiration=END)
        coupon2 = Coupon(rid=12, name="test2", points=20, description="2$ off", begin=BEGIN, expiration=END)
        coupon3 = Coupon(rid=12, name="test3", points=30, description="3$ off", begin=BEGIN, expiration=END)
        db.session.add(coupon1)
        db.session.add(coupon2)
        db.session.add(coupon3)
        db.session.commit()
        coupon_list = couponhelper.get_coupons(15)
        self.assertEqual(coupon_list, [])


if __name__ == "__main__":
    unittest.main()
