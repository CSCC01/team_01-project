import unittest
from app import app
from databaseHelpers.favourite import *

class InsertFavouriteTest(unittest.TestCase):
    '''
    Tests get_favourites(uid): in databaseHelpers/favourite.py.
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

    def test_get_no_favourites(self):
        """
        test user has no favourite restaurants.
        """
        f = Favourite(uid = 3, rid = 8)
        db.session.add(f)
        db.session.commit()
        actual = get_favourites(uid = 4)
        expected = []
        self.assertEqual(actual, expected)


    def test_get_one_favourite(self):
        """
        test user has one favourite restaurant.
        """
        f1 = Favourite(uid = 3, rid = 8)
        f2 = Favourite(uid = 4, rid = 9)
        r1 = Restaurant(rid = 8, name="name1", address="address1", uid=10)
        r2 = Restaurant(rid = 9, name="name2", address="address2", uid=11)
        db.session.add(f1)
        db.session.add(f2)
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()
        actual = get_favourites(uid = 3)
        expected = [
            {
                "rid": 8,
                "name": "name1",
                "address": "address1"
            }
        ]
        self.assertEqual(actual, expected)


    def test_get_many_favourites(self):
        """
        test user has many favourite restaurants.
        """
        f1 = Favourite(uid = 3, rid = 5)
        f2 = Favourite(uid = 3, rid = 7)
        f3 = Favourite(uid = 4, rid = 9)
        r1 = Restaurant(rid = 5, name="name1", address="address1", uid=10)
        r2 = Restaurant(rid = 7, name="name2", address="address2", uid=11)
        db.session.add(f1)
        db.session.add(f2)
        db.session.add(f3)
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()
        actual = get_favourites(uid = 3)
        expected = [
            {
                "rid": 5,
                "name": "name1",
                "address": "address1"
            },
            {
                "rid": 7,
                "name": "name2",
                "address": "address2"
            }
        ]
        self.assertEqual(actual, expected)
