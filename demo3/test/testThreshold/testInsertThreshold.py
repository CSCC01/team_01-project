import unittest

from app import app
from databaseHelpers.threshold import *


class UpdatorThresholdTest(unittest.TestCase):
    '''
    Tests insert_threshold() in databaseHelpers/threshold.py.
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

    def test_insert_valid_threshold(self):
        """
        Test insert a valid row into Thresholds. Expect no error message.
        """
        errmsg = insert_threshold(3, 5, 100)
        expected = Thresholds.query.filter_by(rid = 3, level = 5).first()
        self.assertIsNotNone(expected)
        self.assertEqual(errmsg, [])

    def test_insert_invalid_level(self):
        """
        Test insert an invalid threshold with an empty string as a level. Expect an error message.
        """
        errmsg = insert_threshold(3, "", 100)
        expected_errmsg = ["Invalid level requirment."]
        self.assertEqual(errmsg, expected_errmsg)

    def test_insert_invalid_reward(self):
        """
        Test insert an invalid threshold with an empty string as a reward. Expect an error message.
        """
        errmsg = insert_threshold(3, 5, "")
        expected_null = Thresholds.query.filter_by(rid = 3, level = 5).first()
        expected_errmsg = ["Invalid amount for points."]
        self.assertIsNone(expected_null)
        self.assertEqual(errmsg, expected_errmsg)

    def test_insert_negative_level(self):
        """
        Test insert an invalid threshold with a negative level. Expect an error message.
        """
        errmsg = insert_threshold(3, -5, 100)
        expected_errmsg = ["Invalid level requirment, please provide non-negative value."]
        self.assertEqual(errmsg, expected_errmsg)

    def test_insert_negative_reward(self):
        """
        Test insert an invalid threshold with a negative reward. Expect an error message.
        """
        errmsg = insert_threshold(3, 5, -100)
        expected_null = Thresholds.query.filter_by(rid = 3, level = 5).first()
        expected_errmsg = ["Invalid points, please provide non-negative value."]
        self.assertIsNone(expected_null)
        self.assertEqual(errmsg, expected_errmsg)
