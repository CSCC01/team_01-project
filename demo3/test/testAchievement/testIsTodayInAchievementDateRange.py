import unittest
from app import app
from databaseHelpers.achievement import *
from models import db
from models import Achievements
from datetime import datetime

class DateRangeAchievementTest(unittest.TestCase):
    """
    Test is_today_in_achievement_date_range() in achievement.py.
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

    def test_before_start(self):
        """
        Tests when today's date is before the start date.
        """
        achievement = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=2, value='test;4;False;2099-4-11;2099-4-12')
        self.assertEqual(is_today_in_achievement_date_range(achievement), -1)
    
    def test_on_start(self):
        """
        Tests when today's date is equal to the start date.
        """
        achievement = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=2, value='test;4;False;' + datetime.now().strftime("%Y-%m-%d") + ';2099-4-12')
        self.assertEqual(is_today_in_achievement_date_range(achievement), 0)

    def test_during_range(self):
        """
        Tests when today's date is between the start date and the expiry date.
        """
        achievement = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=2, value='test;4;False;2020-4-11;2099-4-11')
        self.assertEqual(is_today_in_achievement_date_range(achievement), 0)
    
    def test_on_expiry(self):
        """
        Tests when today's date is equal to the expiry date.
        """
        achievement = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=2, value='test;4;False;2020-4-11;' + datetime.now().strftime("%Y-%m-%d"))
        self.assertEqual(is_today_in_achievement_date_range(achievement), 0)

    def test_after_expiry(self):
        """
        Tests when today's date is after the expiry date.
        """
        achievement = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=2, value='test;4;False;2020-4-11;2020-4-12')
        self.assertEqual(is_today_in_achievement_date_range(achievement), 1)

    def test_indefinite_expiry(self):
        """
        Tests when the achievement's expiry date is indefinite.
        """
        achievement = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=2, value='test;4;True;;')
        self.assertEqual(is_today_in_achievement_date_range(achievement), 0)


if __name__ == "__main__":
    unittest.main()
