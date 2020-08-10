import unittest
from app import app
from databaseHelpers.achievement import *
from models import db
from models import Achievements


class TestGetDescp(unittest.TestCase):
    """
    Tests get_achievements_by_rid() in databaseHelpers/achievement.py
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

    def test_get_nonexistent_achievements(self):
        """
        Tests get_achievements_by_rid() when no achievements have a rid
        matching the given rid.
        """
        achievement1 = Achievements(rid=12, name="test", points=10, experience=15, type=0, value="Item;5")
        achievement2 = Achievements(rid=13, name="test 2", points=15, experience=20, type=1, value=";6.99")
        db.session.add(achievement1)
        db.session.add(achievement2)
        db.session.commit()
        achievement_list = get_achievements_by_rid(10)
        self.assertEqual(achievement_list,[])


    def test_get_single_achievements(self):
        """
        Tests get_achievements_by_rid() when one achievement has a rid
        matching the given rid.
        """
        achievement1 = Achievements(rid=12, name="test", points=10, experience=15, type=0, value="Item;5;;;")
        achievement2 = Achievements(rid=13, name="test 2", points=15, experience=20, type=1, value=";6.99;;;")
        db.session.add(achievement1)
        db.session.add(achievement2)
        db.session.commit()
        achievement_list = get_achievements_by_rid(12)
        self.assertEqual(achievement_list,[{'aid': 1,
                     'name': 'test',
                     'points': 10,
                     'experience': 15,
                     'description': "Buy Item 5 times.",
                     'progressMax': 5,
                     'expired': 0}])

        achievement_list = get_achievements_by_rid(13)
        self.assertEqual(achievement_list,[{'aid': 2,
                     'name': 'test 2',
                     'points': 15,
                     'experience': 20,
                     'description': "Spend $6.99 in a single visit.",
                     'progressMax': 1,
                     'expired': 0}])


    def test_get_multiple_achievements(self):
        """
        Tests get_achievements_by_rid() when multiple achievements have a rid matching the given rid.
        """
        achievement1 = Achievements(rid=12, name="test", points=10, experience=15, type=0, value="Item;5;;;")
        achievement2 = Achievements(rid=12, name="test 2", points=15, experience=20, type=1, value=";6.99;;;")
        db.session.add(achievement1)
        db.session.add(achievement2)
        db.session.commit()
        achievement_list = get_achievements_by_rid(12)
        self.assertEqual(achievement_list,[{'aid': 1,
                     'name': 'test',
                     'points': 10,
                     'experience': 15,
                     'description': "Buy Item 5 times.",
                     'progressMax': 5,
                     'expired': 0},
                    {'aid': 2,
                     'name': 'test 2',
                     'points': 15,
                     'experience': 20,
                     'description': "Spend $6.99 in a single visit.",
                     'progressMax': 1,
                     'expired': 0}])


if __name__ == "__main__":
    unittest.main()
