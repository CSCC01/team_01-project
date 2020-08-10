import unittest
from models import Customer_Achievement_Progress, Achievements
from models import db
import time
from datetime import datetime
from app import app
from databaseHelpers import achievementProgress as achievementhelper


class TestGetAchievementsWithProgressData(unittest.TestCase):
    """
    Tests get_achievements_with_progress_data() in achievementProgress.py
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

    def test_get_achievements_progress_data_no_achievements_to_filter(self):
        """
        Tests get_achievements_with_progress_data() when the given achievement list to
        filter is empty.
        """
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=10, progress=3, total=6)
        achievementProgress2 = Customer_Achievement_Progress(uid=5, aid=11, progress=1, total=5)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.commit()

        self.assertEqual(achievementhelper.get_achievements_with_progress_data([], 5), [])

    def test_get_achievements_progress_data_some_achievements_to_filter(self):
        """
        Tests get_achievements_with_progress_data() when the given achievement list to
        filter is not empty
        """
        ac1 = Achievements(aid=11, rid=12, name='test', experience=10, points=15, type=1, value='test')
        ac2 = Achievements(aid=12, rid=12, name='test 2', experience=15, points=20, type=1, value='test')
        ac3 = Achievements(aid=13, rid=12, name='test 3', experience=15, points=15, type=1, value='test')
        db.session.add(ac1)
        db.session.add(ac2)
        db.session.add(ac3)
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=11, progress=2, total=5)
        achievementProgress2 = Customer_Achievement_Progress(uid=5, aid=12, progress=3, total=3)
        achievementProgress3 = Customer_Achievement_Progress(uid=5, aid=13, progress=3, total=6)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.add(achievementProgress3)
        db.session.commit()

        achievement_list = self.achievement_list_helper()
        self.assertEqual(achievementhelper.get_achievements_with_progress_data(achievement_list, 5),
                [{"aid": 10,
            "name": "test",
            "description": "description",
            "experience": 10,
            "points": 15,
            "progressMax": 6,
            "progress": 0,
            "status": 0,
            "expired": 0
            },
            {"aid": 11,
            "name": "test 2",
            "description": "description 2",
            "experience": 15,
            "points": 20,
            "progressMax": 5,
            "progress": 2,
            "status": 1,
            "expired": 0
            },
            {"aid": 12,
            "name": "test 3",
            "description": "description 3",
            "experience": 15,
            "points": 15,
            "progressMax": 3,
            "progress": 3,
            "status": 2,
            "expired": 0
            }])

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
