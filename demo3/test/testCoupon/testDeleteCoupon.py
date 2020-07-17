import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from datetime import datetime
from app import app
from helpers import coupon as couponhelper

BEGIN = datetime.strptime("1 May, 2020", "%d %B, %Y")
END = datetime.strptime("30 June, 2020", "%d %B, %Y")


class DeleteCouponTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_delete_one(self):
        coupon1 = Coupon(rid=12, name="test1", points=10, description="1$ off", begin=BEGIN, expiration=END)
        coupon2 = Coupon(rid=12, name="test2", points=20, description="2$ off", begin=BEGIN, expiration=END)
        db.session.add(coupon1)
        db.session.add(coupon2)
        db.session.commit()
        couponhelper.delete_coupon(1)
        c1 = Coupon.query.filter_by(name="test1").first()
        self.assertIsNone(c1)
        c2 = Coupon.query.filter_by(name="test2").first()
        self.assertIsNotNone(c2)

    def test_delete_many(self):
        coupon1 = Coupon(rid=12, name="test1", points=10, description="1$ off", begin=BEGIN, expiration=END)
        coupon2 = Coupon(rid=14, name="test2", points=20, description="2$ off", begin=BEGIN, expiration=END)
        coupon3 = Coupon(rid=2, name="test3", points=100, description="10$ off", begin=BEGIN, expiration=END)
        coupon4 = Coupon(rid=12, name="test4", points=250, description="25$ off", begin=BEGIN, expiration=END)
        db.session.add(coupon1)
        db.session.add(coupon2)
        db.session.add(coupon3)
        db.session.add(coupon4)
        db.session.commit()
        couponhelper.delete_coupon(1)
        couponhelper.delete_coupon(4)
        c1 = Coupon.query.filter_by(name="test1").first()
        c2 = Coupon.query.filter_by(name="test2").first()
        c3 = Coupon.query.filter_by(name="test3").first()
        c4 = Coupon.query.filter_by(name="test4").first()
        self.assertIsNotNone(c2)
        self.assertIsNotNone(c3)
        self.assertIsNone(c1)
        self.assertIsNone(c4)


if __name__ == "__main__":
    unittest.main()

