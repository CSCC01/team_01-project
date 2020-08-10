import unittest
from app import app
from databaseHelpers.threshold import *

class SelectorThresholdTest(unittest.TestCase):
    '''
    Tests get_thresholds() in databaseHelpers/threshold.py.
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

    def test_no_thresholds(self):
        """
        Test when no threshold is defined for a restaurant. Expect return none.
        """
        t = Thresholds(rid = 3, level = 5, reward = 100)
        db.session.add(t)
        db.session.commit()
        actual = get_thresholds(4)
        expected = []
        self.assertEqual(actual, expected)

    def test_one_threshold(self):
        """
        Test when one threshold is defined for a restaurant. Expect return matching output.
        """
        t = Thresholds(rid = 3, level = 5, reward = 100)
        db.session.add(t)
        db.session.commit()
        actual = get_thresholds(3)
        expected = [{
                "rid": 3,
                "level": 5,
                "reward": 100
            }]
        self.assertEqual(actual, expected)

    def test_many_thresholds(self):
        """
        Test when many thresholds are defined for a restaurant. Expect return matching output.
        """
        t1 = Thresholds(rid = 3, level = 5, reward = 100)
        t2 = Thresholds(rid = 3, level = 10, reward = 300)
        db.session.add(t1)
        db.session.add(t2)
        db.session.commit()
        actual = get_thresholds(3)
        expected = [{
                "rid": 3,
                "level": 5,
                "reward": 100
            },
            {
                "rid": 3,
                "level": 10,
                "reward": 300
            }]
        self.assertEqual(actual, expected)
