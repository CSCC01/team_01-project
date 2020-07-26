import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from datetime import datetime
from app import app
from helpers import coupon

VALID = datetime.strptime("1 May, 9999", "%d %B, %Y")
INVALID = datetime.strptime("30 June, 2020", "%d %B, %Y")


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

    def test_empty_list(self):
        coupons = []
        result = filter_valid_coupons(coupons)
        self.assertEqual(result, [])

    def test_one_valid(self):
        coupons[{
            'expiration': VALID,
            'deleted': 0
        }]
        result = filter_valid_coupons(coupons)
        self.assertEqual(result, coupons)

    def test_many_valid(self):
        coupons[{
            'name': "test coupon"
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
        coupons[{
            'expiration': INVALID,
            'deleted': 0
        }]
        result = filter_valid_coupons(coupons)
        self.assertEqual(result, [])

    def test_one_invalid_deleted(self):
        coupons[{
            'expiration': VALID,
            'deleted': 1
        }]
        result = filter_valid_coupons(coupons)
        self.assertEqual(result, [])

    def test_many_invalid(self):
        coupons[{
            'name': "test coupon"
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
        coupons[{
            'name': "test coupon"
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
        self.assertEqual(result, [{
            'expiration': VALID,
            'deleted': 0
        }])
