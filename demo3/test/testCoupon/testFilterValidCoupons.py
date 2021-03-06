import unittest

from databaseHelpers.coupon import filter_valid_coupons
from models import User, Coupon, Restaurant, Employee
from models import db
import time
import datetime
from app import app

VALID = datetime.date(9999, 5, 1)
INVALID = datetime.date(2020, 6, 30)


class FilterValidCouponTest(unittest.TestCase):
    """
    Test filter_valid_coupons() in databaseHelpers/coupon.py.
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

    def test_empty_list(self):
        """
        Test filtering an empty list.
        """
        coupons = []
        result = filter_valid_coupons(coupons)
        self.assertEqual(result, [])

    def test_one_valid(self):
        """
        Test filtering a list with one item that should not be removed.
        """
        coupons = [{
            'expiration': VALID,
            'deleted': 0
        }]
        result = filter_valid_coupons(coupons)
        self.assertEqual(result, coupons)

    def test_many_valid(self):
        """
        Test filtering a list with many items, all of which should not be removed.
        """
        coupons = [{
            'name': "test coupon",
            'expiration': VALID,
            'deleted': 0
        },
        {
            'expiration': VALID,
            'deleted': 0
        }]
        result = filter_valid_coupons(coupons)
        self.assertEqual(result, coupons)


    def test_one_invalid_date(self):
        """
        Test filtering a list containing one item with an invalid date, the item should be removed.
        """
        coupons = [{
            'expiration': INVALID,
            'deleted': 0
        }]
        result = filter_valid_coupons(coupons)
        self.assertEqual(result, [])

    def test_one_invalid_deleted(self):
        """
        Test filtering a list containing one item that was deleted, the item should be removed.
        """
        coupons = [{
            'expiration': VALID,
            'deleted': 1
        }]
        result = filter_valid_coupons(coupons)
        self.assertEqual(result, [])

    def test_many_invalid(self):
        """
        Test filtering a list with many invalid items, they should all be removed.
        """
        coupons = [{
            'name': "test coupon",
            'expiration': INVALID,
            'deleted': 0
        },
        {
            'expiration': VALID,
            'deleted': 1
        }]
        result = filter_valid_coupons(coupons)
        self.assertEqual(result, [])

    def test_valid_and_invalid(self):
        """
        Test filtering a list with valid and invalid items, only invalid items should be removed.
        """
        coupons = [{
            'name': "test coupon",
            'expiration': VALID,
            'deleted': 0
        },
        {
            'expiration': VALID,
            'deleted': 1
        },
        {
            'expiration': VALID,
            'deleted': 0
        }
        ]
        result = filter_valid_coupons(coupons)
        self.assertEqual(result,
                         [{'deleted': 0, 'expiration': VALID, 'name': 'test coupon'},
                            {'deleted': 0, 'expiration': VALID}])

if __name__ == "__main__":
    unittest.main()
