import unittest
from models import Redeemed_Coupons, Coupon, Restaurant
from models import db
from app import app
from databaseHelpers import redeemedCoupons as rchelper
from databaseHelpers import coupon as chelper


class FindRcidByCidAndUid(unittest.TestCase):
    """
    Test find_rcid_by_cid_and_uid(cid, uid) in redeemedCoupons.py
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

    def test_coupon_diff_user(self):
        """
        Test coupon not redeemed by given user
        """
        rc = Redeemed_Coupons(rcid=121, cid=32, uid=12, rid=12, valid=1)
        db.session.add(rc)
        db.session.commit()
        rcid = rchelper.find_rcid_by_cid_and_uid(32, 10)
        self.assertEqual(rcid, "Not Found")

    def test_coupon_invalid_coupon(self):
        """
        Test coupon with cid and uid but not valid
        """
        rc = Redeemed_Coupons(rcid=121, cid=32, uid=12, rid=12, valid=0)
        db.session.add(rc)
        db.session.commit()
        rcid = rchelper.find_rcid_by_cid_and_uid(32, 12)
        self.assertEqual(rcid, "Not Found")

    def test_mult_coupon_first_valid(self):
        """
        Test for multi redeemed coupons with same cid owned by the same user
        Check if it returns the first valid coupon (rcid)
        """
        rc1 = Redeemed_Coupons(rcid=121, cid=32, uid=12, rid=12, valid=0)
        rc2 = Redeemed_Coupons(rcid=125, cid=32, uid=12, rid=12, valid=1)
        rc3 = Redeemed_Coupons(rcid=129, cid=32, uid=12, rid=12, valid=1)
        db.session.add(rc1)
        db.session.add(rc2)
        db.session.add(rc3)
        db.session.commit()
        rcid = rchelper.find_rcid_by_cid_and_uid(32, 12)
        self.assertEqual(rcid, rc2.rcid)

    def test_normal_resname_valid_cid(self):
        """
        Test if we can find the correct res name by given the cid of the coupon
        as we expected.
        """

        res = Restaurant(name="resName", address="Address", uid=404)
        db.session.add(res)
        db.session.commit()
        coupon = Coupon(rid=res.rid, name="coupon_testing", points=10, description="description", 
                                expiration=None, begin=None, deleted=0)
        db.session.add(coupon)
        db.session.commit()
        rname = chelper.find_res_name_of_coupon_by_cid(coupon.cid)
        self.assertEqual(rname, "resName")

    def test_no_such_cid_name(self):
        """
        Test that this cid is not exist, the method should return 
        "Not Found".
        """
        coupon = Coupon(rid=100, name="coupon_testing", points=25, description="des", 
                                expiration=None, begin=None, deleted=0)
        db.session.add(coupon)
        db.session.commit()
        rname = chelper.find_res_name_of_coupon_by_cid(100)
        self.assertEqual(rname, "Not Found")
    
    def test_no_such_rid_name(self):
        """
        Test that the coupon's related rid is not exist, the method should return 
        "Not Found", the rid is autoincrement, which cannot be negative.
        """
        res = Restaurant(name="resName", address="Address", uid=404)
        db.session.add(res)
        db.session.commit()
        coupon = Coupon(rid=100, name="coupon_testing", points=10, description="description", 
                                expiration=None, begin=None, deleted=0)
        db.session.add(coupon)
        db.session.commit()
        rname = chelper.find_res_name_of_coupon_by_cid(coupon.cid)
        self.assertEqual(rname, "Not Found")

    def test_normal_resaddr_valid_cid(self):
        """
        Test if we can find the correct res addr by given the cid of the coupon
        as we expected.
        """

        res = Restaurant(name="res", address="Address", uid=505)
        db.session.add(res)
        db.session.commit()
        coupon = Coupon(rid=res.rid, name="coupon_testing", points=10, description="description", 
                                expiration=None, begin=None, deleted=0)
        db.session.add(coupon)
        db.session.commit()
        raddr = chelper.find_res_addr_of_coupon_by_cid(coupon.cid)
        self.assertEqual(raddr, "Address")

    def test_no_such_cid_addr(self):
        """
        Test that this cid is not exist, the method should return 
        "Not Found".
        """
        coupon = Coupon(rid=90, name="coupon_testing", points=10, description="description", 
                                expiration=None, begin=None, deleted=0)
        db.session.add(coupon)
        db.session.commit()
        raddr = chelper.find_res_addr_of_coupon_by_cid(120)
        self.assertEqual(raddr, "Not Found")

    def test_no_such_rid_addr(self):
        """
        Test that the coupon's related rid is not exist, the method should return 
        "Not Found".
        """
        res = Restaurant(name="resName", address="Address", uid=404)
        db.session.add(res)
        db.session.commit()
        coupon = Coupon(rid=900, name="coupon_testing", points=10, description="description", 
                                expiration=None, begin=None, deleted=0)
        db.session.add(coupon)
        db.session.commit()
        raddr = chelper.find_res_addr_of_coupon_by_cid(coupon.cid)
        self.assertEqual(raddr, "Not Found")
    


if __name__ == "__main__":
    unittest.main()
