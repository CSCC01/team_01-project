import unittest
from models import Customer_Achievement_Progress, Points, User, Achievements
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

    def test_add_non_complete(self):
        ap = Customer_Achievement_Progress(aid=1, uid=3, progress=1, total=10)
        user = User(uid=3, name='cus', password='passwd', email='test', type=-1)
        points = Points(pid=1, uid=3, rid=1, points=20)
        achievement = Achievements(aid=1, rid=1, name='test', experience=20, points=20, type=0, value='test;10')
        db.session.add(ap)
        db.session.add(user)
        db.session.add(points)
        db.session.add(achievement)
        db.session.commit()
        achievementhelper.add_one_progress_bar(ap)
        self.assertEqual(points.points, 20)
        self.assertEqual(ap.progress, 2)

    def test_add_complete(self):
        ap = Customer_Achievement_Progress(aid=1, uid=3, progress=1, total=2)
        user = User(uid=3, name='cus', password='passwd', email='test', type=-1)
        points = Points(pid=1, uid=3, rid=1, points=20)
        achievement = Achievements(aid=1, rid=1, name='test', experience=20, points=20, type=0, value='test;10')
        db.session.add(ap)
        db.session.add(user)
        db.session.add(points)
        db.session.add(achievement)
        db.session.commit()
        achievementhelper.add_one_progress_bar(ap)
        self.assertEqual(points.points, 40)
        self.assertEqual(ap.progress, 2)

    def test_add_type_one(self):
        ap = Customer_Achievement_Progress(aid=1, uid=3, progress=0, total=1)
        user = User(uid=3, name='cus', password='passwd', email='test', type=-1)
        points = Points(pid=1, uid=3, rid=1, points=20)
        achievement = Achievements(aid=1, rid=1, name='test', experience=20, points=20, type=0, value=';20')
        db.session.add(ap)
        db.session.add(user)
        db.session.add(points)
        db.session.add(achievement)
        db.session.commit()
        achievementhelper.add_one_progress_bar(ap)
        self.assertEqual(points.points, 40)
        self.assertEqual(ap.progress, 1)



if __name__ == "__main__":
    unittest.main()
