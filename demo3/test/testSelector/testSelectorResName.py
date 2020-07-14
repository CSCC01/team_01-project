import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from helpers import selector

class SelectResNameTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_res_name_equal_single(self):
        r1 = Restaurant(name="hhh", address="hhh road", uid=111)
        r2 = Restaurant(name="jjj", address="jjj road", uid=111)
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()
        result = selector.get_resturant_by_name("hhh")
        self.assertEqual(result, r1)


if __name__ == "__main__":
    unittest.main()
