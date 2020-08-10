import unittest
from app import app
from databaseHelpers.achievement import *
from models import db
from models import Achievements


class TestGetProMax(unittest.TestCase):
    """
    Tests get_achievement_progress_maximum() in databaseHelpers/achievement.py
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

    def test_get_progress_max(self):
        """
        Tests get_achievement_progress_maximum() for all achievement types.
        """
        achievement1 = Achievements(rid=12, name="test", points=10, experience=15, type=0, value="Item;5;;;")
        achievement2 = Achievements(rid=13, name="test 2", points=15, experience=20, type=1, value=";6.99;;;")
        achievement3 = Achievements(rid=13, name="test 3", points=15, experience=20, type=2, value=";6;;;")
        achievement4 = Achievements(rid=13, name="test 4", points=15, experience=20, type=3, value=";6;True;;")
        achievement5 = Achievements(rid=13, name="test 5", points=15, experience=20, type=3, value=";6;False;2020-08-1;2020-08-31")

        self.assertEqual(get_achievement_progress_maximum(achievement1), 5)
        self.assertEqual(get_achievement_progress_maximum(achievement2), 1)
        self.assertEqual(get_achievement_progress_maximum(achievement3), 1)
        self.assertEqual(get_achievement_progress_maximum(achievement4), 6)
        self.assertEqual(get_achievement_progress_maximum(achievement5), 6)


if __name__ == "__main__":
    unittest.main()
