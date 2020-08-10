import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from databaseHelpers import restaurant as rhelper


class SelectRidTest(unittest.TestCase):
    '''
    Test get_rid() in databaseHelpers/restaurant.py
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

    def test_owner_found(self):
        """
        Test finding an rid by given a valid uid. Expect output to match correct data.
        """
        restaurant = Restaurant(rid=17465, name="KFC", address="1265 Military trail", uid=34)
        user = User(uid=34, name="joe", email="joe@utsc.com", password="passwd", type=1)
        db.session.add(restaurant)
        db.session.add(user)
        db.session.commit()
        rid = rhelper.get_rid(34)
        self.assertEqual(rid, 17465)

    def test_owner_not_found(self):
        """
        Test finding an rid by given an invalid uid. Expect return none.
        """
        restaurant = Restaurant(rid=17465, name="KFC", address="1265 Military trail", uid=36)
        user1 = User(uid=33, name="joea", email="joea@utsc.com", password="passwd", type=1)
        user2 = User(uid=35, name="joeb", email="joeb@utsc.com", password="passwd", type=1)
        db.session.add(restaurant)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        rid = rhelper.get_rid(34)
        self.assertEqual(rid, None)


if __name__ == "__main__":
    unittest.main()
