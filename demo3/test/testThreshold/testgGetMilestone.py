import unittest
from app import app
from databaseHelpers.threshold import *

class SelectorThresholdTest(unittest.TestCase):
    '''
    Tests get_milestone() in databaseHelpers/threshold.py.
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

    def test_no_milestone(self):
        """
        Test currently no milestone in the database. Expect return none.
        """
        t = Thresholds(rid = 3, level = 5, reward = 100)
        e = Experience(uid = 2, rid = 3, experience = 10000)
        db.session.add(t)
        db.session.add(e)
        db.session.commit()
        actual = get_milestone(2, 3)
        self.assertIsNone(actual)


    def test_valid_milestone(self):
        """
        Test getting the next valid threshold based on a users level. Expect return matching output.
        """
        t = Thresholds(rid = 3, level = 5, reward = 100)
        e = Experience(uid = 2, rid = 3, experience = 0)
        db.session.add(t)
        db.session.add(e)
        db.session.commit()
        actual = get_milestone(2, 3)
        expected = {
            "level": 5,
            "reward": 100
        }
        self.assertEqual(actual, expected)
