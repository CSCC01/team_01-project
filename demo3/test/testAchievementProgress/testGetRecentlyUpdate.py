import unittest
from models import Customer_Achievement_Progress, Achievements, Restaurant
from models import db
from datetime import datetime
from app import app
from databaseHelpers import achievementProgress as achievementhelper
from databaseHelpers import achievement as achelper

NOW = datetime.now()
MAX = datetime.max
MIN = datetime.min
BIG = datetime(2030, 6, 1)
SMALL = datetime(2000, 2, 2)


class GetRecentlyUpdate(unittest.TestCase):
    """
    Tests all methods in achievementProgress.py related to sorting by update datetime
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

    def test_sort_on_short(self):
        """
        test on small data(<=3)
        """
        ap1 = Customer_Achievement_Progress(aid=12, uid=7, progress=2, total=3, update=NOW)
        ap2 = Customer_Achievement_Progress(aid=7, uid=7, progress=1, total=5, update=MIN)
        ap3 = Customer_Achievement_Progress(aid=22, uid=7, progress=5, total=5, update=MAX)
        db.session.add(ap1)
        db.session.add(ap2)
        db.session.add(ap3)
        db.session.commit()
        achievements = achievementhelper.get_recently_update_achievements(7)
        # if sort success, order should be ap3->ap1->ap2
        self.assertEqual(achievements[0].aid, 22)
        self.assertEqual(achievements[1].aid, 12)
        self.assertEqual(achievements[2].aid, 7)

    def test_sort_on_long(self):
        """
        test on big data(>3)
        """
        ap1 = Customer_Achievement_Progress(aid=12, uid=7, progress=2, total=3, update=NOW)
        ap2 = Customer_Achievement_Progress(aid=7, uid=7, progress=1, total=5, update=MIN)
        ap3 = Customer_Achievement_Progress(aid=22, uid=7, progress=5, total=5, update=MAX)
        ap4 = Customer_Achievement_Progress(aid=18, uid=7, progress=2, total=3, update=BIG)
        ap5 = Customer_Achievement_Progress(aid=17, uid=7, progress=1, total=5, update=SMALL)
        db.session.add(ap1)
        db.session.add(ap2)
        db.session.add(ap3)
        db.session.add(ap4)
        db.session.add(ap5)
        db.session.commit()
        achievements = achievementhelper.get_recently_update_achievements(7)
        # if sort success, order should be ap3->ap4->ap1
        self.assertEqual(achievements[0].aid, 22)
        self.assertEqual(achievements[1].aid, 18)
        self.assertEqual(achievements[2].aid, 12)

    def test_get_info(self):
        """
        test on get info function
        """
        ap1 = Customer_Achievement_Progress(aid=12, uid=7, progress=2, total=3, update=NOW)
        ap2 = Customer_Achievement_Progress(aid=7, uid=7, progress=1, total=5, update=BIG)
        a12 = Achievements(aid=12, rid=3, name='10off', experience=10, points=10, type=0, value="coffee;3;False;;")
        a7 = Achievements(aid=7, rid=1, name='20off', experience=1, points=10, type=2, value=";5;False;;")
        r1 = Restaurant(rid=1, name="kfc", address="kfc road", uid=888)
        r3 = Restaurant(rid=3, name="Starbucks", address="Starbucks Road", uid=666)
        db.session.add(ap1)
        db.session.add(ap2)
        db.session.add(a12)
        db.session.add(a7)
        db.session.add(r1)
        db.session.add(r3)
        db.session.commit()
        recent_achievements = achievementhelper.get_recently_update_achievements(7)
        achievement = achievementhelper.get_updated_info(recent_achievements)
        self.assertEqual({'aid': 7,
                       'uid': 7,
                       'progress': 1,
                       'progressMax': 5,
                       'description': 'Visit with a group of at least 5 people.',
                       'name': '20off',
                       'points': 10,
                       'experience': 1,
                       'rname': 'kfc',
                       'raddress': 'kfc road'
                       }, achievement[0])
        self.assertEqual({'aid': 12,
                       'uid': 7,
                       'progress': 2,
                       'progressMax': 3,
                       'description': 'Buy coffee 3 times.',
                       'name': '10off',
                       'points': 10,
                       'experience': 10,
                       'rname': 'Starbucks',
                       'raddress': 'Starbucks Road'
                       }, achievement[1])



if __name__ == "__main__":
    unittest.main()

