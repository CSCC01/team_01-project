import unittest
from app import app
from databaseHelpers.threshold import *

class CheckThresholdTest(unittest.TestCase):
    '''
    Tests check_threshold(rid, level) in databaseHelpers/threshold.py.
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

    def test_check_no_threshold(self):
        """
        Test retreieving an invalid threshold from Threshold table. Expect an error message.
        """
        t = Thresholds(rid = 3, level = 5, reward = 100)
        db.session.add(t)
        db.session.commit()
        actual = check_threshold(3, 4)
        expected = False
        self.assertEqual(actual, expected)

    def test_check_threshold(self):
        """
        Test retreieving a valid threshold from Threshold table. Expect an error message.
        """
        t = Thresholds(rid = 3, level = 5, reward = 100)
        db.session.add(t)
        db.session.commit()
        actual = check_threshold(3, 5)
        expected = True
        self.assertEqual(actual, expected)
