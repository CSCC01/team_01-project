import unittest
from models import Customer_Achievement_Progress, Achievements
from models import db
import time
from datetime import datetime
from app import app
from databaseHelpers import achievementProgress as achievementhelper


class TestGetAchievementProgressbByUid(unittest.TestCase):
    """
    Tests get_achievement_progress_by_uid() in achievementProgress.py
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

    def test_get_nonexistent_achievement_progress(self):
        """
        Tests get_achievement_progress_by_uid() when no achievements have a uid
        matching the given uid.
        """
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=10, progress=3, total=6)
        achievementProgress2 = Customer_Achievement_Progress(uid=6, aid=11, progress=1, total=5)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.commit()
        achievement_progress_list = achievementhelper.get_achievement_progress_by_uid(10)
        self.assertEqual(achievement_progress_list, [])

    def test_get_single_achievement_progress(self):
        """
        Tests get_achievement_progress_by_uid() when one achievement has a uid
        matching the given uid.
        """
        ac1 = Achievements(aid=10, rid=12, name='test1', experience=101, points=101, type=1, value='test')
        ac2 = Achievements(aid=11, rid=12, name='test2', experience=100, points=100, type=1, value='test')
        db.session.add(ac1)
        db.session.add(ac2)
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=10, progress=3, total=6)
        achievementProgress2 = Customer_Achievement_Progress(uid=6, aid=11, progress=1, total=5)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.commit()
        achievement_progress_list = achievementhelper.get_achievement_progress_by_uid(5)
        self.assertEqual(achievement_progress_list, [{'aid': 10,
                                                      'progress': 3,
                                                      'progressMax': 6,
                                                      'uid': 5, 'update': None}])

        achievement_list = achievementhelper.get_achievement_progress_by_uid(6)
        self.assertEqual(achievement_list, [{'aid': 11,
                                             'progress': 1,
                                             'progressMax': 5,
                                             'uid': 6, 'update': None}])

    def test_get_multiple_achievement_progress(self):
        """
        Tests get_achievement_progress_by_uid() when multiple achievements have a uid
        matching the given uid.
        """
        ac1 = Achievements(aid=10, rid=12, name='test1', experience=101, points=101, type=1, value='test')
        ac2 = Achievements(aid=11, rid=12, name='test2', experience=100, points=100, type=1, value='test')
        db.session.add(ac1)
        db.session.add(ac2)
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=10, progress=3, total=6)
        achievementProgress2 = Customer_Achievement_Progress(uid=5, aid=11, progress=1, total=5)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.commit()
        achievement_progress_list = achievementhelper.get_achievement_progress_by_uid(5)
        self.assertEqual(achievement_progress_list, [{'aid': 10,
                                                      'progress': 3,
                                                      'progressMax': 6,
                                                      'uid': 5, 'update': None},
                                                     {'aid': 11,
                                                      'progress': 1,
                                                      'progressMax': 5,
                                                      'uid': 5, 'update': None}])

    def achievement_list_helper(self):
        return [{"aid": 10,
                 "name": "test",
                 "description": "description",
                 "experience": 10,
                 "points": 15,
                 "progressMax": 6,
                 "expired": 0
                 },
                {"aid": 11,
                 "name": "test 2",
                 "description": "description 2",
                 "experience": 15,
                 "points": 20,
                 "progressMax": 5,
                 "expired": 0
                 },
                {"aid": 12,
                 "name": "test 3",
                 "description": "description 3",
                 "experience": 15,
                 "points": 15,
                 "progressMax": 3,
                 "expired": 0
                 }]


if __name__ == "__main__":
    unittest.main()
