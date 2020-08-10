import unittest

from app import app
from databaseHelpers.threshold import *


class UpdatorThresholdTest(unittest.TestCase):
    '''
    Tests delete_threshold(rid, level) in databaseHelpers/threshold.py.
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

    def test_remove_invalid_threshold(self):
        """
        Test removing a row that does not exist in the Threshold table. Expect the object is still in database.
        """
        t = Thresholds(rid = 3, level = 5, reward = 100)
        db.session.add(t)
        db.session.commit()
        delete_threshold(3, 10)
        expected = Thresholds.query.filter_by(rid = 3, level = 5).first()
        self.assertIsNotNone(expected)

    def test_remove_valid_threshold(self):
        """
        Test removing a valid row from the Threshold table. Expect successfully removed.
        """
        t = Thresholds(rid = 3, level = 5, reward = 100)
        db.session.add(t)
        db.session.commit()
        delete_threshold(3, 5)
        expected = Thresholds.query.filter_by(rid = 3, level = 5).first()
        self.assertIsNone(expected)
