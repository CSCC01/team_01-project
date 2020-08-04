import unittest
from app import app
from databaseHelpers.achievement import *
from models import db
from models import Achievements
from datetime import datetime

BEGIN = datetime.strptime("1 May, 2020", "%d %B, %Y")
END_VALID = datetime.strptime("30 June, 2099", "%d %B, %Y")
END_EXPIRED = datetime.strptime("30 June, 2019", "%d %B, %Y")


class DeleteExpiredAchievementTest(unittest.TestCase):
    """
    Test function on delete expired achievement.
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
        """No coupons in the achievement table are expired. No coupons are removed"""
        ac1 = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=3, value='test;4;False;2020-4-11;2099-4-11')
        ac2 = Achievements(aid=22, rid=12, name='test', experience=10, points=10, type=3, value='test;5;False;2020-4-1;2099-4-11')
        db.session.add(ac1)
        db.session.add(ac2)
        db.session.commit()
        delete_expired_achievements(12)
        a1 = Achievements.query.filter_by(aid=32).first()
        a2 = Achievements.query.filter_by(aid=22).first()
        self.assertIsNotNone(a1)
        self.assertIsNotNone(a2)


    def test_one_expired_achievement(self):
        """One coupon in the achievement table are expired. The expired coupon is removed."""
        ac1 = Achievements(rid=12, name='test', experience=10, points=10, type=3, value='test;4;False;2020-4-11;2020-4-11')
        ac2 = Achievements(rid=12, name='test', experience=10, points=10, type=3, value='test;5;False;2020-04-1;2099-04-11')
        db.session.add(ac1)
        db.session.add(ac2)
        db.session.commit()
        delete_expired_achievements(12)
        a1 = Achievements.query.filter_by(aid=ac1.aid).first()
        a2 = Achievements.query.filter_by(aid=ac2.aid).first()
        self.assertIsNone(a1)
        self.assertIsNotNone(a2)

    def test_many_expired_achievements(self):
        """Many coupons in the achievement table are expired. The expired coupons are removed."""
        ac1 = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=3, value='test;4;False;2020-4-11;2020-4-11')
        ac2 = Achievements(aid=22, rid=12, name='test', experience=10, points=10, type=3, value='test;5;False;2020-04-1;2020-04-11')
        db.session.add(ac1)
        db.session.add(ac2)
        db.session.commit()
        delete_expired_achievements(12)
        a1 = Achievements.query.filter_by(aid=32).first()
        a2 = Achievements.query.filter_by(aid=22).first()
        self.assertIsNone(a1)
        self.assertIsNone(a2)


if __name__ == "__main__":
    unittest.main()
