import unittest
from app import app
from databaseHelpers.favourite import *

class InsertFavouriteTest(unittest.TestCase):
    '''
    Tests add_favourite(uid, rid) in databaseHelpers/favourite.py.
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

    def test_insert(self):
        """
        test insert a row into Favourite.
        """
        add_favourite(uid = 3, rid = 5)
        fav = Favourite.query.filter_by(uid = 3, rid = 5).first()
        self.assertEqual(fav.uid, 3)
        self.assertEqual(fav.rid, 5)
