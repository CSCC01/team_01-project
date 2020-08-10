import unittest
from models import Customer_Achievement_Progress, Achievements
from models import db
import time
from datetime import datetime
from app import app
from databaseHelpers import achievementProgress as achievementhelper


class TestGetAchievementWithProgressData(unittest.TestCase):
    """
    Tests get_achievement_with_progress_data() in achievementProgress.py
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

    def test_get_achievement_with_progress_data_by_nonexistent_aid(self):
        '''
        Tests get_achievement_with_progress_data(aid, uid) for an aid that
        does not match any achievement.
        '''
        self.assertIsNone(achievementhelper.get_achievement_with_progress_data(5, 6), None)
        

    def test_get_achievement_with_progress_data_by_uid_with_no_progress(self):
        '''
        Tests get_achievement_with_progress_data(aid, uid) for a uid that
        does not match any achievement progress entry.
        '''
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
        '''
        Tests get_achievement_with_progress_data(aid, uid) for a uid that
        does not match any achievement progress entry for the given aid.
        '''
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
        '''
        Tests get_achievement_with_progress_data(aid, uid) for an existing
        aid and an existing customer progress entry.
        '''
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
