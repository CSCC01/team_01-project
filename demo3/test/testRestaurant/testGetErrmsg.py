import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from databaseHelpers.restaurant import *


class InsertRestaurantTest(unittest.TestCase):
    '''
    Test insert_new_restaurant() in databaseHelpers/restaurant.py
    '''
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_no_errmsg(self):
        """Tests that valid input results in no errors"""
        actual = get_errmsg("name", "address", [])
        expected = []
        self.assertEqual(actual, expected)

    def test_invalid_name(self):
        """Test that invalid name results in name error"""
        actual = get_errmsg("", "address", ["something"])
        expected = ["something", "A restaurant name is required."]
        self.assertEqual(actual, expected)

    def test_invalid_address(self):
        """Tests that invalid address results in address error"""
        actual = get_errmsg("name", "", [])
        expected = ["A restaurant address is required."]
        self.assertEqual(actual, expected)

    def test_invalid_name_and_address(self):
        """Tests that invalid name and address results in errors"""
        actual = get_errmsg("", "", ["something"])
        expected = ["something", "A restaurant name is required.", "A restaurant address is required."]
        self.assertEqual(actual, expected)
