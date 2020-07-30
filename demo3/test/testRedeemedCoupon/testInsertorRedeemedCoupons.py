"""
Test suite for databaseHelpers.redeemedCoupons.py's insert_redeemed_coupon function.
"""


import unittest

from databaseHelpers.redeemedCoupons import insert_redeemed_coupon
from models import User, Coupon, Restaurant, Employee, Redeemed_Coupons
from models import db
import time
from app import app
from databaseHelpers import redeemedCoupons
from datetime import datetime

class InsertRedeemedCouponTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_insert_coupon(self):
        """
        Testing inserting an arbitrary coupon.
        """
        cid = 3
        rid = 5
        uid = 6
        rcid = insert_redeemed_coupon(cid, uid, rid)
        coupon = Redeemed_Coupons.query.filter_by(rcid = rcid).first()
        self.assertIsNotNone(coupon)
        self.assertEqual(coupon.cid, 3)
        self.assertEqual(coupon.rid, 5)
        self.assertEqual(coupon.uid, 6)
        self.assertEqual(coupon.valid, 1)

if __name__ == "__main__":
    unittest.main()
