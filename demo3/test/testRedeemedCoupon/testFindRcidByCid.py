import unittest
from models import Redeemed_Coupons
from models import db
from app import app
from helpers import redeemedCoupons as rchelper


class FindRcidByCidAndUid(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_one_coupon(self):
        """
        Test with one standard coupon
        """
        rc = Redeemed_Coupons(rcid=18, cid=32, uid=12, rid=12, valid=1)
        db.session.add(rc)
        db.session.commit()
        rcid = rchelper.find_rcid_by_cid_and_uid(rc.cid,rc.uid)
        self.assertEqual(rcid, rc.rcid)

    def test_many_coupon_same_cid(self):
        """
        Test with many coupons of the same cid
        """
        rc1 = Redeemed_Coupons(rcid=121, cid=32, uid=12, rid=12, valid=1)
        rc2 = Redeemed_Coupons(rcid=131238, cid=32, uid=15, rid=12, valid=1)
        db.session.add(rc1)
        db.session.add(rc2)
        db.session.commit()
        rcid1 = rchelper.find_rcid_by_cid_and_uid(rc1.cid, rc1.uid)
        rcid2 = rchelper.find_rcid_by_cid_and_uid(rc2.cid, rc2.uid)
        self.assertEqual(rcid1, rc1.rcid)
        self.assertEqual(rcid2, rc2.rcid)

    def test_many_coupon_same_user(self):
        """
        Test with many coupons of the same uid
        """
        rc1 = Redeemed_Coupons(rcid=121, cid=32, uid=12, rid=12, valid=1)
        rc2 = Redeemed_Coupons(rcid=131238, cid=36, uid=12, rid=12, valid=1)
        db.session.add(rc1)
        db.session.add(rc2)
        db.session.commit()
        rcid1 = rchelper.find_rcid_by_cid_and_uid(rc1.cid, rc1.uid)
        rcid2 = rchelper.find_rcid_by_cid_and_uid(rc2.cid, rc2.uid)
        self.assertEqual(rcid1, rc1.rcid)
        self.assertEqual(rcid2, rc2.rcid)


if __name__ == "__main__":
    unittest.main()