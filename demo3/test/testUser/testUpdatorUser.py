import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from databaseHelpers.user import *

class SelectUserTest(unittest.TestCase):
    '''
    Tests update_type() in databaseHelpers/user.py.
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

    def test_no_user(self):
        """
        Testing with a uid that does not exist in the database. Expect return none
        """
        actual = update_type(5, 2)
        self.assertIsNone(actual)

    def test_valid_user(self):
        """
        Testing with a uid that does exist in the database. Expect successfully updated.
        """
        user = User(uid=5, name="joe", email="joe.com", password="omit", type=0)
        db.session.add(user)
        db.session.commit()
        actual = update_type(5, 2)
        type = User.query.filter_by(uid=5).first().type
        self.assertIsNone(actual)
        self.assertEqual(type, 2)
