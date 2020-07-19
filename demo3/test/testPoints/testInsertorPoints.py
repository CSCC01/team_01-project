import unittest
from models import User, Restaurant, Points
from models import db
import time
from app import app
from helpers import points as pointshelper

class InsertPointsTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_insert_standard_points_entry(self):
        errmsg = pointshelper.insert_points(1, 12)
        self.assertEqual(errmsg, None)

        points = Points.query.filter_by(pid=1).first()
        self.assertNotEqual(points, None)
        self.assertEqual(points.pid, 1)
        self.assertEqual(points.uid, 1)
        self.assertEqual(points.rid, 12)
        self.assertEqual(points.points, 0)
    
    def test_insert_duplicate_uid_points_entry(self):
        points = Points(uid=1, rid=12, points=10)
        db.session.add(points)
        errmsg = pointshelper.insert_points(1, 13)
        self.assertEqual(errmsg, None)

        points = Points.query.filter_by(uid=1)
        self.assertEqual(points.count(), 2)

        points = Points.query.filter_by(pid=1).first()
        self.assertNotEqual(points, None)
        self.assertEqual(points.uid, 1)
        self.assertEqual(points.rid, 12)
        self.assertEqual(points.points, 10)

        points = Points.query.filter_by(pid=2).first()
        self.assertNotEqual(points, None)
        self.assertEqual(points.uid, 1)
        self.assertEqual(points.rid, 13)
        self.assertEqual(points.points, 0)

    def test_insert_duplicate_rid_points_entry(self):
        points = Points(uid=1, rid=12, points=10)
        db.session.add(points)
        errmsg = pointshelper.insert_points(2, 12)
        self.assertEqual(errmsg, None)

        points = Points.query.filter_by(rid=12)
        self.assertEqual(points.count(), 2)

        points = Points.query.filter_by(pid=1).first()
        self.assertNotEqual(points, None)
        self.assertEqual(points.uid, 1)
        self.assertEqual(points.rid, 12)
        self.assertEqual(points.points, 10)

        points = Points.query.filter_by(pid=2).first()
        self.assertNotEqual(points, None)
        self.assertEqual(points.uid, 2)
        self.assertEqual(points.rid, 12)
        self.assertEqual(points.points, 0)
    
    def test_insert_duplicate_uid_and_rid_points_entry(self):
        points = Points(uid=1, rid=12, points=10)
        db.session.add(points)
        errmsg = pointshelper.insert_points(1, 12)
        self.assertEqual(errmsg, ["Points entry already exists for given user at this restaurant."])

        points = Points.query.filter_by(uid=1, rid=12)
        self.assertEqual(points.count(), 1)
        self.assertEqual(points.first().pid, 1)
        self.assertEqual(points.first().uid, 1)
        self.assertEqual(points.first().rid, 12)
        self.assertEqual(points.first().points, 10)
    



if __name__ == "__main__":
    unittest.main()
