"""

Test suite for helper.coupon.py's get_coupons function.

"""



import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
import datetime
from app import app
from databaseHelpers import coupon as couponhelper

BEGIN = datetime.date(2020, 5, 1)
END = datetime.date(2020, 6, 30)


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
        """
        Retives coupon list when there is only one.
        """
        coupon = Coupon(rid=12, name="test", points=10, description="1$ off", level=1, begin=BEGIN, expiration=END, deleted=0)
        db.session.add(coupon)
        db.session.commit()
        coupon_list = couponhelper.get_coupons(12)
        self.assertEqual(coupon_list,[{'begin': BEGIN,
                     'cid': 1,
                     'description': '1$ off',
                     'expiration': END,
                     'name': 'test',
                     'points': 10,
                     'level': 1,
                     "deleted": 0}])

    def test_coupon_multi(self):
        """
        Retives coupon list when there are many.
        """
        coupon1 = Coupon(rid=12, name="test1", points=10, description="1$ off", level=1, begin=BEGIN, expiration=END, deleted=0)
        coupon2 = Coupon(rid=12, name="test2", points=20, description="2$ off", level=2, begin=BEGIN, expiration=END, deleted=1)
        coupon3 = Coupon(rid=12, name="test3", points=30, description="3$ off", level=3, begin=BEGIN, expiration=END, deleted=0)
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
                     'points': 10,
                     'level': 1,
                     "deleted": 0},
                    {'begin': BEGIN,
                     'cid': 2,
                     'description': '2$ off',
                     'expiration': END,
                     'name': 'test2',
                     'points': 20,
                     'level': 2,
                     "deleted": 1},
                    {'begin': BEGIN,
                     'cid': 3,
                     'description': '3$ off',
                     'expiration': END,
                     'name': 'test3',
                     'points': 30,
                     'level': 3,
                     "deleted": 0}])

    def test_coupon_none(self):
        """
        Retives coupon list when there are none.
        """
        coupon1 = Coupon(rid=12, name="test1", points=10, description="1$ off", level=1, begin=BEGIN, expiration=END, deleted=0)
        coupon2 = Coupon(rid=12, name="test2", points=20, description="2$ off", level=10, begin=BEGIN, expiration=END, deleted=0)
        coupon3 = Coupon(rid=12, name="test3", points=30, description="3$ off", level=100, begin=BEGIN, expiration=END, deleted=1)
        db.session.add(coupon1)
        db.session.add(coupon2)
        db.session.add(coupon3)
        db.session.commit()
        coupon_list = couponhelper.get_coupons(15)
        self.assertEqual(coupon_list, [])


if __name__ == "__main__":
    unittest.main()
