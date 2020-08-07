import unittest
from app import app
from databaseHelpers.favourite import *

class InsertFavouriteTest(unittest.TestCase):
    '''
    Tests remove_faviourite(uid, rid) in databaseHelpers/favourite.py.
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

    def test_remove_invalid_favourite(self):
        """
        test removing a row that do not exist in the Favourite's table.
        """
        f = Favourite(uid = 3, rid = 5)
        db.session.add(f)
        db.session.commit()
        remove_faviourite(uid = 3, rid = 6)
        fav = Favourite.query.filter_by(uid = 3, rid = 5).first()
        self.assertEqual(fav.uid, 3)
        self.assertEqual(fav.rid, 5)

    def test_remove_valid_favourite(self):
        """
        test removing a valid row from the Favourite's table.
        """
        f = Favourite(uid = 3, rid = 5)
        db.session.add(f)
        db.session.commit()
        remove_faviourite(uid = 3, rid = 5)
        fav = Favourite.query.filter_by(uid = 3, rid = 5).first()
        self.assertIsNone(fav)
