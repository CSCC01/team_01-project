import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from helpers import restaurant as rhelper

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
        result = rhelper.get_resturant_by_name("hhh")
        self.assertIn({'name': 'hhh', 'address': 'hhh road', 'rid': 1}, result)
        self.assertNotIn({'name': 'jjj', 'address': 'jjj road', 'rid': 2}, result)

    def test_res_name_equal_many(self):
        r1 = Restaurant(name="hhh", address="hhh road", uid=111)
        r2 = Restaurant(name="hhh", address="jjj road", uid=111)
        r3 = Restaurant(name="hhh", address="ggg road", uid=222)
        db.session.add(r1)
        db.session.add(r2)
        db.session.add(r3)
        db.session.commit()
        result = rhelper.get_resturant_by_name("hhh")
        self.assertIn({'name': 'hhh', 'address': 'hhh road', 'rid': 1}, result)
        self.assertIn({'name': 'hhh', 'address': 'jjj road', 'rid': 2}, result)
        self.assertIn({'name': 'hhh', 'address': 'ggg road', 'rid': 3}, result)

    def test_res_name_part_single(self):
        r1 = Restaurant(name="hhh restaurant", address="hhh road", uid=111)
        r2 = Restaurant(name="jjj restaurant", address="jjj road", uid=111)
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()
        result = rhelper.get_resturant_by_name("hhh")
        self.assertIn({'name': 'hhh restaurant', 'address': 'hhh road', 'rid': 1}, result)
        self.assertNotIn({'name': 'jjj restaurant', 'address': 'jjj road', 'rid': 2}, result)

    def test_res_name_part_name(self):
        r1 = Restaurant(name="kfc kfc kfc", address="hhh road", uid=111)
        r2 = Restaurant(name="kfc", address="jjj road", uid=111)
        r3 = Restaurant(name="Kentucky Fried Chicken", address="ggg road", uid=222)
        db.session.add(r1)
        db.session.add(r2)
        db.session.add(r3)
        db.session.commit()
        result = rhelper.get_resturant_by_name("kfc")
        self.assertIn({'name': 'kfc kfc kfc', 'address': 'hhh road', 'rid': 1}, result)
        self.assertIn({'name': 'kfc', 'address': 'jjj road', 'rid': 2}, result)
        self.assertNotIn({'name': 'kentucky Fried Chicken', 'address': 'ggg road', 'rid': 3}, result)

    def test_res_name_none(self):
        r1 = Restaurant(name="hhh restaurant", address="hhh road", uid=111)
        r2 = Restaurant(name="jjj restaurant", address="jjj road", uid=111)
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()
        result = rhelper.get_resturant_by_name("ggg")
        self.assertNotIn({'name': 'hhh restaurant', 'address': 'hhh road', 'rid': 1}, result)
        self.assertNotIn({'name': 'jjj restaurant', 'address': 'jjj road', 'rid': 2}, result)


if __name__ == "__main__":
    unittest.main()
