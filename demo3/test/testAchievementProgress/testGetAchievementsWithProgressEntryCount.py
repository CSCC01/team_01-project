import unittest
from models import Customer_Achievement_Progress, Points, User, Achievements
from models import db
from app import app
from databaseHelpers import achievementProgress as achievementhelper


class testGetAchievementsWithProgressEntryCount(unittest.TestCase):
    """
    Tests get_achievements_with_progress_entry_count() in achievementProgress.py
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

    def test_achievement_list_empty(self):
        '''
        Tests appending progress entry count data to an empty achievement
        list.
        '''
        progress = Customer_Achievement_Progress(aid=1, uid=3, progress=3, total=4)
        db.session.add(progress)
        db.session.commit()

        self.assertEqual(achievementhelper.get_achievements_with_progress_entry_count([]), [])
        

    def test_no_progress_on_any_achievements(self):
        '''
        Tests appending progress entry count data to an achievement list
        where none of the achievements have progress entries
        '''
        progress = Customer_Achievement_Progress(aid=1, uid=3, progress=3, total=4)
        db.session.add(progress)
        db.session.commit()

        achievement_list = self.achievement_list_helper()
        self.assertEqual(achievementhelper.get_achievements_with_progress_entry_count(achievement_list),
            [{"aid": 10,
            "name": "test",
            "description": "description",
            "experience": 10,
            "points": 15,
            "progressMax": 6,
            "expired": 0,
            "progress_entries": 0
            },
            {"aid": 11,
            "name": "test 2",
            "description": "description 2",
            "experience": 15,
            "points": 20,
            "progressMax": 5,
            "expired": 0,
            "progress_entries": 0
            },
            {"aid": 12,
            "name": "test 3",
            "description": "description 3",
            "experience": 15,
            "points": 15,
            "progressMax": 3,
            "expired": 0,
            "progress_entries": 0
            }])

    def test_some_achievements_have_progress(self):
        '''
        Tests appending progress entry count data to an achievement list
        where some of the achievements have progress entries
        '''
        progress1 = Customer_Achievement_Progress(aid=10, uid=3, progress=4, total=6)
        progress2 = Customer_Achievement_Progress(aid=10, uid=4, progress=6, total=6)
        progress3 = Customer_Achievement_Progress(aid=11, uid=4, progress=1, total=5)

        db.session.add(progress1)
        db.session.add(progress2)
        db.session.add(progress3)
        db.session.commit()

        achievement_list = self.achievement_list_helper()
        self.assertEqual(achievementhelper.get_achievements_with_progress_entry_count(achievement_list),
            [{"aid": 10,
            "name": "test",
            "description": "description",
            "experience": 10,
            "points": 15,
            "progressMax": 6,
            "expired": 0,
            "progress_entries": 2
            },
            {"aid": 11,
            "name": "test 2",
            "description": "description 2",
            "experience": 15,
            "points": 20,
            "progressMax": 5,
            "expired": 0,
            "progress_entries": 1
            },
            {"aid": 12,
            "name": "test 3",
            "description": "description 3",
            "experience": 15,
            "points": 15,
            "progressMax": 3,
            "expired": 0,
            "progress_entries": 0
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
