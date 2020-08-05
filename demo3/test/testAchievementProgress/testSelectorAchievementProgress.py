import unittest
from models import Customer_Achievement_Progress, Achievements
from models import db
import time
from datetime import datetime
from app import app
from databaseHelpers import achievementProgress as achievementhelper


class SelectCustomerAchievementProgressTest(unittest.TestCase):
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

    def test_get_achievements_progress_data_no_achievements_to_filter(self):
        """Tests get_achievements_with_progress_data() when the given achievement list to
        filter is empty."""
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=10, progress=3, total=6)
        achievementProgress2 = Customer_Achievement_Progress(uid=5, aid=11, progress=1, total=5)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.commit()

        self.assertEqual(achievementhelper.get_achievements_with_progress_data([], 5), [])

    def test_get_achievements_progress_data_some_achievements_to_filter(self):
        """Tests get_achievements_with_progress_data() when the given achievement list to
        filter is not empty"""
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

    def test_get_recent_achievements_no_achievements_to_filter(self):
        """Tests get_recently_started_achievements() when the given achievement list to
        filter is empty."""
        achievementProgress1 = Customer_Achievement_Progress(uid=5, aid=10, progress=3, total=6)
        achievementProgress2 = Customer_Achievement_Progress(uid=5, aid=11, progress=1, total=5)
        db.session.add(achievementProgress1)
        db.session.add(achievementProgress2)
        db.session.commit()

        self.assertEqual(achievementhelper.get_recently_started_achievements([], 5), [])

    def test_get_recent_achievements_no_progress_to_filter(self):
        """Tests get_recently_started_achievements() when the given user has no progress entries."""
        achievement_list = self.achievement_list_helper()
        self.assertEqual(achievementhelper.get_recently_started_achievements(achievement_list, 5), [])

    def test_get_recent_achievements_no_relevant_achievements_to_filter(self):
        """Tests get_recently_started_achievements() when the user does not have progress relevant
        to the achievements in the given achievement list."""
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
        """Tests get_recently_started_achievements() when the user has less than three incomplete
        progress entries relevant to the given achievement list."""
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
        """Tests get_recently_started_achievements() when the user has exactly three incomplete
        progress entries relevant to the given achievement list."""
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
        """Tests get_recently_started_achievements() when the user has more than three incomplete
        progress entries relevant to the given achievement list."""
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


    def test_get_achievement_with_progress_data_by_nonexistent_aid(self):
        '''Tests get_achievement_with_progress_data(aid, uid) for an aid that
        does not match any achievement.'''
        self.assertIsNone(achievementhelper.get_achievement_with_progress_data(5, 6), None)
        

    def test_get_achievement_with_progress_data_by_uid_with_no_progress(self):
        '''Tests get_achievement_with_progress_data(aid, uid) for a uid that
        does not match any achievement progress entry.'''
        achievement = Achievements(rid=12, name="test", points=10, experience=15, type=0, value="Item;5;;;")
        db.session.add(achievement)
        db.session.commit()

        self.assertEqual(achievementhelper.get_achievement_with_progress_data(1, 6), 
            {
                "aid": 1,
                "name": "test",
                "description": "Buy Item 5 times.",
                "experience": 15,
                "points": 10,
                "progressMax": 5,
                "progress": 0
            })


    
    def test_get_achievement_with_progress_data_by_uid_with_no_relevant_progress(self):
        '''Tests get_achievement_with_progress_data(aid, uid) for a uid that
        does not match any achievement progress entry for the given aid.'''
        achievement = Achievements(rid=12, name="test", points=10, experience=15, type=0, value="Item;5;;;")
        achievementProgress = Customer_Achievement_Progress(uid=6, aid=11, progress=2, total=5)
        db.session.add(achievement)
        db.session.add(achievementProgress)
        db.session.commit()

        self.assertEqual(achievementhelper.get_achievement_with_progress_data(1, 6), 
            {
                "aid": 1,
                "name": "test",
                "description": "Buy Item 5 times.",
                "experience": 15,
                "points": 10,
                "progressMax": 5,
                "progress": 0
            })
    

    def test_get_achievement_with_progress_data_with_valid_aid_and_progress(self):
        '''Tests get_achievement_with_progress_data(aid, uid) for an existing
        aid and an existing customer progress entry.'''
        achievement = Achievements(rid=12, name="test", points=10, experience=15, type=0, value="Item;5;;;")
        achievementProgress = Customer_Achievement_Progress(uid=6, aid=1, progress=2, total=5)
        db.session.add(achievement)
        db.session.add(achievementProgress)
        db.session.commit()

        self.assertEqual(achievementhelper.get_achievement_with_progress_data(1, 6), 
            {
                "aid": 1,
                "name": "test",
                "description": "Buy Item 5 times.",
                "experience": 15,
                "points": 10,
                "progressMax": 5,
                "progress": 2
            })

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
