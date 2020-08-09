import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from databaseHelpers import restaurant as rhelper


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

    def test_insert_one_restaurant(self):
        """
        Test insert a normal restaurant without any issue. Expect output to match correct data in database.
        """
        rid = rhelper.insert_new_restaurant("KFC", "1265 Military Trail", 2)
        restaurant = Restaurant.query.filter_by(name="KFC").first()
        self.assertIsNotNone(restaurant)
        self.assertEqual(rid, 1)
        r1 = Restaurant.query.filter_by(rid=rid).first()
        self.assertEqual(r1.name, "KFC")
        self.assertEqual(r1.address, "1265 Military Trail")
        self.assertEqual(r1.uid, 2)

    def test_insert_many_restaurant(self):
        """
        Test insert multi normal restaurant without any issue. Expect output to match correct data in database.
        """
        rid1 = rhelper.insert_new_restaurant("KFC", "1265 Military Trail", 2)
        rid2 = rhelper.insert_new_restaurant("MacDonald's", "1278 Military Trail", 2)
        rid3 = rhelper.insert_new_restaurant("CFK", "5621 Gh Drive", 4)
        rid4 = rhelper.insert_new_restaurant("KFC", "88 Borough Ave", 12)
        self.assertEqual(rid1, 1)
        self.assertEqual(rid2, 2)
        self.assertEqual(rid3, 3)
        self.assertEqual(rid4, 4)

        r1 = Restaurant.query.filter_by(rid=rid1).first()
        self.assertEqual(r1.name, "KFC")
        self.assertEqual(r1.address, "1265 Military Trail")
        self.assertEqual(r1.uid, 2)

        r2 = Restaurant.query.filter_by(rid=rid2).first()
        self.assertEqual(r2.name, "MacDonald's")
        self.assertEqual(r2.address, "1278 Military Trail")
        self.assertEqual(r2.uid, 2)

        r3 = Restaurant.query.filter_by(rid=rid3).first()
        self.assertEqual(r3.name, "CFK")
        self.assertEqual(r3.address, "5621 Gh Drive")
        self.assertEqual(r3.uid, 4)

        r4 = Restaurant.query.filter_by(rid=rid4).first()
        self.assertEqual(r4.name, "KFC")
        self.assertEqual(r4.address, "88 Borough Ave")
        self.assertEqual(r4.uid, 12)


if __name__ == "__main__":
    unittest.main()
