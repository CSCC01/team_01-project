import unittest
from models import Redeemed_Coupons
from models import db
from app import app
from databaseHelpers import redeemedCoupons as rchelper


class MarkRedeemedCoupon(unittest.TestCase):
    """
    Test mark_redeem_coupon_used_by_rcid(rcid) in redeemedCoupons.py
    """
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_valid_coupon(self):
        """
        Test mark on one valid coupon. Expect output to match correct data.
        """
        rc = Redeemed_Coupons(cid=32, uid=12, rid=12, valid=1)
        db.session.add(rc)
        db.session.commit()
        rchelper.mark_redeem_coupon_used_by_rcid(1)
        self.assertEqual(rc.valid, 0)


    def test_invalid_coupon(self):
        """
        Test function also works on invalid coupon. Expect data in database remain the same
        """
        rc1 = Redeemed_Coupons(cid=32, uid=12, rid=12, valid=0)
        db.session.add(rc1)
        db.session.commit()
        rchelper.mark_redeem_coupon_used_by_rcid(1)
        self.assertEqual(rc1.valid, 0)


if __name__ == "__main__":
    unittest.main()
