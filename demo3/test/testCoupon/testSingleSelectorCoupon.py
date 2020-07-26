import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
from datetime import datetime
from app import app
from helpers import coupon as couponhelper

BEGIN = datetime.strptime("1 May, 2020", "%d %B, %Y")
END = datetime.strptime("30 June, 2020", "%d %B, %Y")


class SingleSelectorCouponTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_coupon_none(self):
        coupon = Coupon(rid=12, name="test", points=10, description="1$ off", begin=BEGIN, expiration=END)
        db.session.add(coupon)
        db.session.commit()

        result = couponhelper.get_coupon_by_cid(coupon.cid + 2)
        self.assertEqual(result, None)

    def test_coupon_single(self):
        coupon = Coupon(rid=12, name="test", points=10, description="1$ off", begin=BEGIN, expiration=END, deleted=0)
        db.session.add(coupon)
        db.session.commit()

        result = couponhelper.get_coupon_by_cid(coupon.cid)
        self.assertEqual(result,
                            {"cid": coupon.cid,
                             "cname": coupon.name,
                             "cdescription": coupon.description,
                             "begin": coupon.begin,
                             "expiration": coupon.expiration
                             })

    def test_coupon_none(self):
        result = couponhelper.get_coupon_by_cid(5)
        self.assertEqual(result, None)


if __name__ == "__main__":
    unittest.main()
