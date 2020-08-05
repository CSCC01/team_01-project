import unittest
from app import app
import databaseHelpers.achievement import *
from models import db
from models import Achievements
from datetime import datetime

class IsExpiredAchievementTest(unittest.TestCase):
    """
    Test suite for the function is_achievement_expired in achievement.py.
    """
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_before_expiry(self):
        """Tests when today's date is before the expiry date."""
        achievement = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=3, value='test;4;False;2020-4-11;2099-4-11')
        self.assertEqual(is_achievement_expired(achievement), False)

    def test_on_expiry(self):
        """Tests when today's date is equal to the expiry date."""
        achievement = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=3, value='test;4;False;2020-4-11;' + now.strftime("%Y-%m-%d"))
        self.assertEqual(is_achievement_expired(achievement), False)

    def test_after_expiry(self):
        """Tests when today's date is after the expiry date."""
        achievement = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=3, value='test;4;False;2020-4-11;2020-4-12')
        self.assertEqual(is_achievement_expired(achievement), True)

    def test_indefinite_expiry(self):
        """Tests when the achievement's expiry date is indefinite."""
        achievement = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=3, value='test;4;True;;' + now.strftime("%Y-%m-%d"))
        self.assertEqual(is_achievement_expired(achievement), False)

    def test_not_expirable(self):
        """Tests when the achievement type has no date data."""
        achievement1 = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=0, value='test;4;;;' + now.strftime("%Y-%m-%d"))
        achievement2 = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=1, value='test;4;;;' + now.strftime("%Y-%m-%d"))
        achievement3 = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=2, value='test;4;;;' + now.strftime("%Y-%m-%d"))
        
        self.assertEqual(is_achievement_expired(achievement1), False)
        self.assertEqual(is_achievement_expired(achievement2), False)
        self.assertEqual(is_achievement_expired(achievement3), False)



if __name__ == "__main__":
    unittest.main()
