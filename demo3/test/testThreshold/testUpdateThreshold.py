import unittest

from app import app
from databaseHelpers.threshold import *


class UpdatorThresholdTest(unittest.TestCase):
    '''
    Tests update_threshold(rid, level, reward) in databaseHelpers/threshold.py.
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
        
    def test_update_negative_reward_threshold(self):
        """
        Test updating a threshold with a negative reward. Expect an error message.
        """
        t = Thresholds(rid = 3, level = 5, reward = 100)
        db.session.add(t)
        db.session.commit()
        errmsg = update_threshold(3, 5, -200)
        expected = ["Invalid points, please provide non-negative value."]
        self.assertEqual(errmsg, expected)

    def test_update_negative_level_threshold(self):
        """
        Test updating a threshold with a negative level. Expect an error message.
        """
        t = Thresholds(rid = 3, level = 5, reward = 100)
        db.session.add(t)
        db.session.commit()
        errmsg = update_threshold(3, -5, 200)
        expected = ["Invalid level requirment, please provide non-negative value."]
        self.assertEqual(errmsg, expected)

    def test_update_invalid_reward_threshold(self):
        """
        Test updating that reward with an empty string. Expect an error message.
        """
        t = Thresholds(rid = 3, level = 5, reward = 100)
        db.session.add(t)
        db.session.commit()
        errmsg = update_threshold(3, 5, "")
        expected = ["Invalid amount for points."]
        self.assertEqual(errmsg, expected)

    def test_update_invalid_level_threshold(self):
        """
        Test updating the level with an empty string. Expect an error message.
        """
        t = Thresholds(rid = 3, level = 5, reward = 100)
        db.session.add(t)
        db.session.commit()
        errmsg = update_threshold(3, "", 200)
        expected = ["Invalid level requirment."]
        self.assertEqual(errmsg, expected)

    def test_update_valid_threshold(self):
        """
        Test updating a valid threshold. Expect successful update.
        """
        t = Thresholds(rid = 3, level = 5, reward = 100)
        db.session.add(t)
        db.session.commit()
        errmsg = update_threshold(3, 5, 200)
        self.assertEqual(errmsg, [])
        actual = Thresholds.query.filter_by(rid = 3, level = 5, reward = 200).first()
        self.assertIsNotNone(actual)
