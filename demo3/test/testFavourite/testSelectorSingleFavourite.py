import unittest
from app import app
from databaseHelpers.favourite import *

class InsertFavouriteTest(unittest.TestCase):
    '''
    Tests check_favourite(uid, rid) in databaseHelpers/favourite.py.
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

    def test_get_no_favourite(self):
        """
        Test retrieveing an invalid favourite from the table. Expect output to match correct data.
        """
        f = Favourite(uid = 3, rid = 5)
        db.session.add(f)
        db.session.commit()
        actual = check_favourite(uid=4, rid=7)
        expected = False
        self.assertEqual(actual, expected)


    def test_get_favourite(self):
        """
        Test retrieveing a valid favourite from the table. Expect output to match correct data.
        """
        f = Favourite(uid = 3, rid = 5)
        db.session.add(f)
        db.session.commit()
        actual = check_favourite(uid=3, rid=5)
        expected = True
        self.assertEqual(actual, expected)
