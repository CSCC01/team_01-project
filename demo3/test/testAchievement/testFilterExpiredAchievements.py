import unittest
from app import app
from databaseHelpers.achievement import *
from models import db
from models import Achievements
from datetime import datetime

BEGIN = datetime.strptime("1 May, 2020", "%d %B, %Y")
END_VALID = datetime.strptime("30 June, 2099", "%d %B, %Y")
END_EXPIRED = datetime.strptime("30 June, 2019", "%d %B, %Y")


class FilterExpiredAchievementTest(unittest.TestCase):
    """
    Test suite for the function filter_expired_achievements in achievement.py.
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

    def test_no_expired_achievements(self):
        """No achievements in the achievement table are expired. All achievements should show up."""
        ac1 = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=3, value='test;4;False;2020-4-11;2099-4-11')
        ac2 = Achievements(aid=22, rid=12, name='test', experience=10, points=10, type=3, value='test;5;False;2020-4-1;2099-4-11')
        db.session.add(ac1)
        db.session.add(ac2)
        db.session.commit()
        result = filter_expired_achievements(12)
        expected = [{
                    "aid": 22,
                    "name": "test",
                    "description": "Visit 5 times between 2020-4-1 and 2099-4-11.",
                    "experience": 10,
                    "points": 10,
                    "progressMax": 5},
                  {
                    "aid": 32,
                    "name": "test",
                    "description": "Visit 4 times between 2020-4-11 and 2099-4-11.",
                    "experience": 10,
                    "points": 10,
                    "progressMax": 4}
                 ]
        self.assertEqual(result, expected)




    def test_one_expired_achievement(self):
        """One achievement in the achievement table are expired. Expired achievement should not be in list."""
        ac1 = Achievements(aid = 32, rid=12, name='test', experience=10, points=10, type=3, value='test;4;False;2020-4-11;2020-4-11')
        ac2 = Achievements(aid = 22, rid=12, name='test', experience=10, points=10, type=3, value='test;5;False;2020-4-1;2099-4-11')
        db.session.add(ac1)
        db.session.add(ac2)
        db.session.commit()
        result = filter_expired_achievements(12)
        expected = [{
                    "aid": 22,
                    "name": "test",
                    "description": "Visit 5 times between 2020-4-1 and 2099-4-11.",
                    "experience": 10,
                    "points": 10,
                    "progressMax": 5}
                 ]
        self.assertEqual(result, expected)


    def test_many_expired_achievements(self):
        """Many coupons in the achievement table are expired. The expired achievements should not be in list."""
        ac1 = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=3, value='test;4;False;2020-4-11;2020-4-11')
        ac2 = Achievements(aid=22, rid=12, name='test', experience=10, points=10, type=2, value='test;5;False;2020-04-1;2020-04-11')
        db.session.add(ac1)
        db.session.add(ac2)
        db.session.commit()
        result = filter_expired_achievements(12)
        expected = []
        self.assertEqual(result, expected)



if __name__ == "__main__":
    unittest.main()
