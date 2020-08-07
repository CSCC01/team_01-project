import unittest
from app import app
from databaseHelpers.coupon import *
from models import db
from models import Coupon
from datetime import datetime

class DateRangeCouponTest(unittest.TestCase):
    """
    Test suite for the function is_today_in_coupon_date_range() in coupon.py.
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

    def test_before_start(self):
        """Tests when today's date is before the start date."""
        begin = date(2099, 5, 1)
        end = date(2099, 6, 30)
        coupon = Coupon(rid=12, name="test", points=10, description="1$ off", begin=begin, expiration=end, deleted=0)
        self.assertEqual(is_today_in_coupon_date_range(coupon), -1)
    
    def test_on_start(self):
        """Tests when today's date is equal to the start date."""
        begin = date.today()
        end = date(2099, 6, 30)
        coupon = Coupon(rid=12, name="test", points=10, description="1$ off", begin=begin, expiration=end, deleted=0)
        self.assertEqual(is_today_in_coupon_date_range(coupon), 0)

    def test_during_range(self):
        """Tests when today's date is between the start date and the expiry date."""
        begin = date(2020, 5, 1)
        end = date(2099, 6, 30)
        coupon = Coupon(rid=12, name="test", points=10, description="1$ off", begin=begin, expiration=end, deleted=0)
        self.assertEqual(is_today_in_coupon_date_range(coupon), 0)
    
    def test_on_expiry(self):
        """Tests when today's date is equal to the expiry date."""
        begin = date(2020, 5, 1)
        end = date.today()
        coupon = Coupon(rid=12, name="test", points=10, description="1$ off", begin=begin, expiration=end, deleted=0)
        self.assertEqual(is_today_in_coupon_date_range(coupon), 0)

    def test_after_expiry(self):
        """Tests when today's date is after the expiry date."""
        begin = date(2020, 5, 1)
        end = date(2020, 6, 30)
        coupon = Coupon(rid=12, name="test", points=10, description="1$ off", begin=begin, expiration=end, deleted=0)
        self.assertEqual(is_today_in_coupon_date_range(coupon), 1)

    def test_indefinite_expiry(self):
        """Tests when the coupon's expiry date is indefinite."""
        coupon = Coupon(rid=12, name="test", points=10, description="1$ off", begin=None, expiration=None, deleted=0)
        self.assertEqual(is_today_in_coupon_date_range(coupon), 0)


if __name__ == "__main__":
    unittest.main()
