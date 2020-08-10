import unittest
from models import Customer_Achievement_Progress, Achievements
from models import db
from app import app
from databaseHelpers.achievementProgress import *


class GetProgressCompletionStatusTest(unittest.TestCase):
    """
    Tests get_achievement_progress_stats(achievements) in achievementProgress.py
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

    def test_no_achievements(self):
        """
        Test an empty list of achievements
        """
        achievement_list = []
        actual = get_achievement_progress_stats(achievement_list)
        expected = []
        self.assertEqual(actual, expected)

    def test_one_achievement(self):
        """
        Test a list of one achievement
        """
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=10, progress=3, total=3)
        achievementProgress2 = Customer_Achievement_Progress(uid=6, aid=10, progress=2, total=3)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.commit()
        achievement_list = [{
            "aid": 10,
            "name": "testing",
            "description": "This is just for a test",
            "experience": 50,
            "points": 100,
            "progressMax": 3,
            "expired": False
        }]
        actual = get_achievement_progress_stats(achievement_list)
        expected = [{
            "aid": 10,
            "name": "testing",
            "description": "This is just for a test",
            "experience": 50,
            "points": 100,
            "progressMax": 3,
            "expired": False,
            "in progress": 1,
            "complete": 1
        }]
        self.assertEqual(actual, expected)

    def test_many_achievements(self):
        """
        Test a list of many coupons
        """
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=10, progress=3, total=3)
        achievementProgress2 = Customer_Achievement_Progress(uid=6, aid=10, progress=2, total=3)
        achievementProgress3 = Customer_Achievement_Progress(uid=6, aid=11, progress=2, total=6)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.add(achievementProgress3)
        db.session.commit()
        achievement_list = [{
            "aid": 10,
            "name": "testing",
            "description": "This is just for a test",
            "experience": 50,
            "points": 100,
            "progressMax": 3,
            "expired": False
            }, {
            "aid": 11,
            "name": "another test",
            "description": "This is just for a test",
            "experience": 200,
            "points": 50,
            "progressMax": 6,
            "expired": True
        }]
        actual = get_achievement_progress_stats(achievement_list)
        expected = [{
            "aid": 10,
            "name": "testing",
            "description": "This is just for a test",
            "experience": 50,
            "points": 100,
            "progressMax": 3,
            "expired": False,
            "in progress": 1,
            "complete": 1
        }, {
            "aid": 11,
            "name": "another test",
            "description": "This is just for a test",
            "experience": 200,
            "points": 50,
            "progressMax": 6,
            "expired": True,
            "in progress": 1,
            "complete": 0
        }]
        self.assertEqual(actual, expected)
