import unittest
from models import Customer_Achievement_Progress, Achievements
from models import db
import time
from datetime import datetime
from app import app
from databaseHelpers import achievementProgress as achievementhelper


class TestGetRecentlyStartedAchievements(unittest.TestCase):
    """
    Tests get_recently_started_achievements() in achievementProgress.py
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

    def test_get_recent_achievements_no_achievements_to_filter(self):
        """
        Tests get_recently_started_achievements() when the given achievement list to
        filter is empty.
        """
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=10, progress=3, total=6)
        achievementProgress2 = Customer_Achievement_Progress(uid=5, aid=11, progress=1, total=5)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.commit()

        self.assertEqual(achievementhelper.get_recently_started_achievements([], 5), [])

    def test_get_recent_achievements_no_progress_to_filter(self):
        """
        Tests get_recently_started_achievements() when the given user has no progress entries.
        """
        achievement_list = self.achievement_list_helper()
        self.assertEqual(achievementhelper.get_recently_started_achievements(achievement_list, 5), [])

    def test_get_recent_achievements_no_relevant_achievements_to_filter(self):
        """
        Tests get_recently_started_achievements() when the user does not have progress relevant
        to the achievements in the given achievement list.
        """
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=5, progress=2, total=5)
        achievementProgress2 = Customer_Achievement_Progress(uid=6, aid=12, progress=1, total=3)
        achievementProgress3 = Customer_Achievement_Progress(uid=5, aid=13, progress=3, total=6)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.add(achievementProgress3)
        db.session.commit()

        achievement_list = self.achievement_list_helper()
        self.assertEqual(achievementhelper.get_recently_started_achievements(achievement_list, 5),[])

    def test_get_recent_achievements_only_complete_achievements(self):
        """Tests get_recently_started_achievements() when the user only has complete progress (progress
        = progressMax) relevant to the achievements in the given achievement list."""
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=11, progress=5, total=5)
        achievementProgress2 = Customer_Achievement_Progress(uid=5, aid=12, progress=3, total=3)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.commit()

        achievement_list = self.achievement_list_helper()
        self.assertEqual(achievementhelper.get_recently_started_achievements(achievement_list, 5),[])

    def test_get_recent_achievements_less_than_three_matches(self):
        """
        Tests get_recently_started_achievements() when the user has less than three incomplete
        progress entries relevant to the given achievement list.
        """
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=11, progress=2, total=5)
        achievementProgress2 = Customer_Achievement_Progress(uid=5, aid=12, progress=1, total=3)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.commit()

        achievement_list = self.achievement_list_helper()
        self.assertEqual(achievementhelper.get_recently_started_achievements(achievement_list, 5),
        [{"aid": 12,
            "name": "test 3",
            "description": "description 3",
            "experience": 15,
            "points": 15,
            "progressMax": 3,
            "progress": 1,
            "status": 1,
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
            }])
    
    def test_get_recent_achievements_three_matches(self):
        """
        Tests get_recently_started_achievements() when the user has exactly three incomplete
        progress entries relevant to the given achievement list.
        """
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=11, progress=2, total=5)
        achievementProgress2 = Customer_Achievement_Progress(uid=5, aid=12, progress=1, total=3)
        achievementProgress3 = Customer_Achievement_Progress(uid=5, aid=10, progress=2, total=6)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.add(achievementProgress3)
        db.session.commit()

        achievement_list = self.achievement_list_helper()
        self.assertEqual(achievementhelper.get_recently_started_achievements(achievement_list, 5),
        [{"aid": 10,
            "name": "test",
            "description": "description",
            "experience": 10,
            "points": 15,
            "progressMax": 6,
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
            "progress": 1,
            "status": 1,
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
            }])
    
    def test_get_recent_achievements_more_than_three_matches(self):
        """
        Tests get_recently_started_achievements() when the user has more than three incomplete
        progress entries relevant to the given achievement list.
        """
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=11, progress=2, total=5)
        achievementProgress2 = Customer_Achievement_Progress(uid=5, aid=12, progress=1, total=3)
        achievementProgress3 = Customer_Achievement_Progress(uid=5, aid=10, progress=2, total=6)
        achievementProgress4 = Customer_Achievement_Progress(uid=5, aid=20, progress=5, total=6)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.add(achievementProgress3)
        db.session.add(achievementProgress4)
        db.session.commit()

        achievement_list = self.achievement_list_helper()
        achievement_list.append({ "aid": 20,
                                    "name": "test 4",
                                    "description": "description 4",
                                    "experience": 5,
                                    "points": 5,
                                    "progressMax": 6,
                                    "expired": 0})

        self.assertEqual(achievementhelper.get_recently_started_achievements(achievement_list, 5),
        [{"aid": 20,
            "name": "test 4",
            "description": "description 4",
            "experience": 5,
            "points": 5,
            "progressMax": 6,
            "expired": 0,
            "progress": 5,
            "status": 1
            },
            {"aid": 10,
            "name": "test",
            "description": "description",
            "experience": 10,
            "points": 15,
            "progressMax": 6,
            "expired": 0,
            "progress": 2,
            "status": 1
            },
            {"aid": 12,
            "name": "test 3",
            "description": "description 3",
            "experience": 15,
            "points": 15,
            "progressMax": 3,
            "expired": 0,
            "progress": 1,
            "status": 1
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
