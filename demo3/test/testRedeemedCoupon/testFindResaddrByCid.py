import unittest
from models import Coupon, Restaurant
from models import db
from app import app
from databaseHelpers import coupon as chelper


class FindResaddrByCid(unittest.TestCase):
    """
    Test find_res_addr_of_coupon_by_cid() in redeemedCoupons.py
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
    
    def test_normal_resaddr_valid_cid(self):
        """
        Test if we can find the correct res addr by given the cid of the coupon
        as we expected. Expect output to match correct data.
        """
        res = Restaurant(name="res", address="Address", uid=505)
        db.session.add(res)
        db.session.commit()
        coupon = Coupon(rid=res.rid, name="coupon_testing", points=10, description="description", 
                        level=56, expiration=None, begin=None, deleted=0)
        db.session.add(coupon)
        db.session.commit()
        raddr = chelper.find_res_addr_of_coupon_by_cid(coupon.cid)
        self.assertEqual(raddr, "Address")

    def test_no_such_cid_addr(self):
        """
        Test that this cid is not exist, the method should return 
        "Not Found". Expect an error message.
        """
        coupon = Coupon(rid=90, name="coupon_testing", points=10, description="description", 
                        level=2, expiration=None, begin=None, deleted=0)
        db.session.add(coupon)
        db.session.commit()
        raddr = chelper.find_res_addr_of_coupon_by_cid(120)
        self.assertEqual(raddr, "Not Found")

    def test_no_such_rid_addr(self):
        """
        Test that the coupon's related rid is not exist, the method should return 
        "Not Found". Expect an error message.
        """
        res = Restaurant(name="resName", address="Address", uid=404)
        db.session.add(res)
        db.session.commit()
        coupon = Coupon(rid=900, name="coupon_testing", points=10, description="description", 
                        level=88, expiration=None, begin=None, deleted=0)
        db.session.add(coupon)
        db.session.commit()
        raddr = chelper.find_res_addr_of_coupon_by_cid(coupon.cid)
        self.assertEqual(raddr, "Not Found")
