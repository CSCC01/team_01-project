import unittest
from models import Customer_Achievement_Progress
from models import db
import time
from datetime import datetime
from app import app
from databaseHelpers import achievementProgress as achievementhelper


class SelectCustomer_Achievement_ProgressTest(unittest.TestCase):
    """
    Tests all methods in achievementProgress.py related to selecting achievement progress
    using the achievement progress table.
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
        """Tests get_achievement_progress_by_uid() when no achievements have a uid
        matching the given uid."""
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=10, progress=3, total=6)
        achievementProgress2 = Customer_Achievement_Progress(uid=6, aid=11, progress=1, total=5)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.commit()
        achievement_progress_list = achievementhelper.get_achievement_progress_by_uid(10)
        self.assertEqual(achievement_progress_list,[])

    def test_get_single_achievement_progress(self):
        """Tests get_achievement_progress_by_uid() when one achievement has a uid
        matching the given uid."""
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=10, progress=3, total=6)
        achievementProgress2 = Customer_Achievement_Progress(uid=6, aid=11, progress=1, total=5)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.commit()
        achievement_progress_list = achievementhelper.get_achievement_progress_by_uid(5)
        self.assertEqual(achievement_progress_list,[{'aid': 10,
                     'progress': 3,
                     'progressMax': 6}])

        achievement_list = achievementhelper.get_achievement_progress_by_uid(6)
        self.assertEqual(achievement_list,[{'aid': 11,
                     'progress': 1,
                     'progressMax': 5}])

    def test_get_multiple_achievement_progress(self):
        """Tests get_achievement_progress_by_uid() when multiple achievements have a uid
        matching the given uid."""
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=10, progress=3, total=6)
        achievementProgress2 = Customer_Achievement_Progress(uid=5, aid=11, progress=1, total=5)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.commit()
        achievement_progress_list = achievementhelper.get_achievement_progress_by_uid(5)
        self.assertEqual(achievement_progress_list,[{'aid': 10,
                     'progress': 3,
                     'progressMax': 6},
                    {'aid': 11,
                     'progress': 1,
                     'progressMax': 5}])

    def test_filter_no_progress_achievements_no_achievements_to_filter(self):
        """Tests get_achievements_with_no_progress() when the given achievement list to
        filter is empty."""
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=10, progress=3, total=6)
        achievementProgress2 = Customer_Achievement_Progress(uid=5, aid=11, progress=1, total=5)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.commit()

        self.assertEqual(achievementhelper.get_achievements_with_no_progress([], 5), [])

    def test_filter_no_progress_achievements_all_achievements_have_progress(self):
        """Tests get_achievements_with_no_progress() when all achievements in the given
        achievement list have progress."""
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=10, progress=3, total=6)
        achievementProgress2 = Customer_Achievement_Progress(uid=5, aid=11, progress=1, total=5)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.commit()

        achievement_list = self.achievement_list_helper()
        self.assertEqual(achievementhelper.get_achievements_with_no_progress(achievement_list, 5),[])

    def test_filter_no_progress_achievements_some_achievements_have_progress(self):
        """Tests get_achievements_with_no_progress() when some but not all achievements in
        the given achievement list have progress."""
        achievementProgress = Customer_Achievement_Progress(uid=5, aid=10, progress=3, total=6)
        db.session.add(achievementProgress)
        db.session.commit()

        achievement_list = self.achievement_list_helper()
        self.assertEqual(achievementhelper.get_achievements_with_no_progress(achievement_list, 5),
                            [{"aid": 11,
                            "name": "test 2",
                            "description": "description 2",
                            "experience": 15,
                            "points": 20,
                            "progressMax": 5,
                            "progress": 0,
                            }])

    def test_filter_no_progress_achievements_no_achievements_have_progress(self):
        """Tests get_achievements_with_no_progress() when no achievements in the given
        achievement list have progress."""
        achievement_list = self.achievement_list_helper()
        self.assertEqual(achievementhelper.get_achievements_with_no_progress(achievement_list, 5),
                            [{"aid": 10,
                            "name": "test",
                            "description": "description",
                            "experience": 10,
                            "points": 15,
                            "progressMax": 6,
                            "progress": 0
                            },
                            {"aid": 11,
                            "name": "test 2",
                            "description": "description 2",
                            "experience": 15,
                            "points": 20,
                            "progressMax": 5,
                            "progress": 0
                            }])

    def achievement_list_helper(self):
        return [{"aid": 10,
            "name": "test",
            "description": "description",
            "experience": 10,
            "points": 15,
            "progressMax": 6
            },
            {"aid": 11,
            "name": "test 2",
            "description": "description 2",
            "experience": 15,
            "points": 20,
            "progressMax": 5
            }]

if __name__ == "__main__":
    unittest.main()
