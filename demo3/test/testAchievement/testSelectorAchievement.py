import unittest
from app import app
from databaseHelpers.achievement import *
from models import db
from models import Achievements


class SelectAchievementTest(unittest.TestCase):
    """
    Tests all methods in achievement.py related to selecting achievements
    from the achievement table.
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

    def test_get_values(self):
        """Tests get_achievement_values() for all achievement types."""
        achievement1 = Achievements(rid=12, name="test", points=10, experience=15, type=0, value="Item;5;;;")
        achievement2 = Achievements(rid=13, name="test 2", points=15, experience=20, type=1, value=";6.99;;;")
        achievement3 = Achievements(rid=13, name="test 3", points=15, experience=20, type=2, value=";6;;;")
        achievement4 = Achievements(rid=13, name="test 3", points=15, experience=20, type=2, value=";6;True;;")
        achievement5 = Achievements(rid=13, name="test 3", points=15, experience=20, type=2, value=";6;False;2020-08-1;2020-08-31")

        self.assertEqual(get_achievement_data(achievement1), ["Item", "5", "", "", ""])
        self.assertEqual(get_achievement_data(achievement2), ["", "6.99", "", "", ""])
        self.assertEqual(get_achievement_data(achievement3), ["", "6", "", "", ""])
        self.assertEqual(get_achievement_data(achievement4), ["", "6", "True", "", ""])
        self.assertEqual(get_achievement_data(achievement5), ["", "6", "False", "2020-08-1", "2020-08-31"])


    def test_get_description(self):
        """Tests get_achievement_description() for all achievement types."""
        achievement1 = Achievements(rid=12, name="test", points=10, experience=15, type=0, value="Item;5;True;;")
        achievement2 = Achievements(rid=13, name="test 2", points=15, experience=20, type=1, value=";6.99;True;;")
        achievement3 = Achievements(rid=13, name="test 3", points=15, experience=20, type=2, value=";2;True;;")
        achievement4 = Achievements(rid=13, name="test 4", points=15, experience=20, type=3, value=";5;True;;")
        achievement5 = Achievements(rid=12, name="test 5", points=10, experience=15, type=0, value="Item;5;False;2020-08-01;2020-08-31")
        achievement6 = Achievements(rid=13, name="test 6", points=15, experience=20, type=1, value=";6.99;False;2020-08-01;2020-08-31")
        achievement7 = Achievements(rid=13, name="test 7", points=15, experience=20, type=2, value=";2;False;2020-08-01;2020-08-31")
        achievement8 = Achievements(rid=13, name="test 8", points=15, experience=20, type=3, value=";5;False;2020-08-01;2020-08-31")

        self.assertEqual(get_achievement_description(achievement1), "Buy Item 5 times.")
        self.assertEqual(get_achievement_description(achievement2), "Spend $6.99 in a single visit.")
        self.assertEqual(get_achievement_description(achievement3), "Visit with a group of at least 2 people.")
        self.assertEqual(get_achievement_description(achievement4), "Visit 5 times.")
        self.assertEqual(get_achievement_description(achievement5), "Buy Item 5 times between 2020-08-01 and 2020-08-31.")
        self.assertEqual(get_achievement_description(achievement6), "Spend $6.99 in a single visit between 2020-08-01 and 2020-08-31.")
        self.assertEqual(get_achievement_description(achievement7), "Visit with a group of at least 2 people between 2020-08-01 and 2020-08-31.")
        self.assertEqual(get_achievement_description(achievement8), "Visit 5 times between 2020-08-01 and 2020-08-31.")


    def test_get_progress_max(self):
        """Tests get_achievement_progress_maximum() for all achievement types."""
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


    def test_get_nonexistent_achievements(self):
        """Tests get_achievements_by_rid() when no achievements have a rid
        matching the given rid."""
        achievement1 = Achievements(rid=12, name="test", points=10, experience=15, type=0, value="Item;5")
        achievement2 = Achievements(rid=13, name="test 2", points=15, experience=20, type=1, value=";6.99")
        db.session.add(achievement1)
        db.session.add(achievement2)
        db.session.commit()
        achievement_list = get_achievements_by_rid(10)
        self.assertEqual(achievement_list,[])


    def test_get_single_achievements(self):
        """Tests get_achievements_by_rid() when one achievement has a rid
        matching the given rid."""
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
        """Tests get_achievements_by_rid() when multiple achievements have a rid matching the given rid."""
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
