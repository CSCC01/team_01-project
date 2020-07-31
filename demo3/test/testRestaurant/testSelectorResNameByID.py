import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from databaseHelpers import restaurant as rhelper


class SelectResNameByID(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_res_name_not_found(self):
        restaurant = Restaurant(rid = 96, name = "bla", address = "1234 Main street", uid = 758)
        db.session.add(restaurant)
        db.session.commit()
        name = rhelper.get_restaurant_name_by_rid(259)
        self.assertEqual(name, None)

    def test_res_name_found(self):
        restaurant = Restaurant(rid = 96, name = "bla", address = "1234 Main street", uid = 758)
        db.session.add(restaurant)
        db.session.commit()
        name = rhelper.get_restaurant_name_by_rid(96)
        self.assertEqual(name, "bla")

if __name__ == "__main__":
    unittest.main()

