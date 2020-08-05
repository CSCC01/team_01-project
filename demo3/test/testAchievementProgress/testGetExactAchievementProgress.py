import unittest
from models import Customer_Achievement_Progress
from models import db
from app import app
from databaseHelpers import achievementProgress as achievementhelper


class Get_Exact_Customer_Achievement_ProgressTest(unittest.TestCase):
    """
    Tests the get method in achievementProgress.py
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

    def test_normal_found(self):
        achievement_progress = Customer_Achievement_Progress(aid=17, uid=4, progress=3, total=5)
        db.session.add(achievement_progress)
        db.session.commit()
        a = achievementhelper.get_exact_achivement_progress(aid=17, uid=4)
        self.assertEqual(a.aid, achievement_progress.aid)
        self.assertEqual(a.uid, achievement_progress.uid)
        self.assertEqual(a.progress, achievement_progress.progress)
        self.assertEqual(a.total, achievement_progress.total)

    def test_found_with_same_uid(self):
        ap1 = Customer_Achievement_Progress(aid=17, uid=4, progress=3, total=5)
        ap2 = Customer_Achievement_Progress(aid=18, uid=4, progress=3, total=5)
        db.session.add(ap1)
        db.session.add(ap2)
        db.session.commit()
        a = achievementhelper.get_exact_achivement_progress(aid=17, uid=4)
        self.assertEqual(a.aid, ap1.aid)
        self.assertEqual(a.uid, ap1.uid)
        self.assertEqual(a.progress, ap1.progress)
        self.assertEqual(a.total, ap1.total)

    def test_found_with_same_aid(self):
        ap1 = Customer_Achievement_Progress(aid=18, uid=4, progress=3, total=5)
        ap2 = Customer_Achievement_Progress(aid=18, uid=8, progress=3, total=5)
        db.session.add(ap1)
        db.session.add(ap2)
        db.session.commit()
        a = achievementhelper.get_exact_achivement_progress(aid=18, uid=8)
        self.assertEqual(a.aid, ap2.aid)
        self.assertEqual(a.uid, ap2.uid)
        self.assertEqual(a.progress, ap2.progress)
        self.assertEqual(a.total, ap2.total)


    def test_aid_not_found(self):
        achievement_progress = Customer_Achievement_Progress(aid=17, uid=4, progress=3, total=5)
        db.session.add(achievement_progress)
        db.session.commit()
        a = achievementhelper.get_exact_achivement_progress(aid=15, uid=4)
        self.assertEqual(a, 'Not Found')

    def test_uid_not_found(self):
        achievement_progress = Customer_Achievement_Progress(aid=17, uid=4, progress=3, total=5)
        db.session.add(achievement_progress)
        db.session.commit()
        a = achievementhelper.get_exact_achivement_progress(aid=17, uid=5)
        self.assertEqual(a, 'Not Found')



if __name__ == "__main__":
    unittest.main()
