import unittest
from models import Coupon, Restaurant
from models import db
from app import app
from databaseHelpers import coupon as chelper


class FindResnameByCid(unittest.TestCase):
    """
    Test find_res_name_of_coupon_by_cid() in redeemedCoupons.py
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

    def test_normal_resname_valid_cid(self):
        """
        Test if we can find the correct res name by given the cid of the coupon
        as we expected.
        """

        res = Restaurant(name="resName", address="Address", uid=404)
        db.session.add(res)
        db.session.commit()
        coupon = Coupon(rid=res.rid, name="coupon_testing", points=10, description="description",
                        level=250, expiration=None, begin=None, deleted=0)
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
                        level=36, expiration=None, begin=None, deleted=0)
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
                        level=99, expiration=None, begin=None, deleted=0)
        db.session.add(coupon)
        db.session.commit()
        rname = chelper.find_res_name_of_coupon_by_cid(coupon.cid)
        self.assertEqual(rname, "Not Found")
