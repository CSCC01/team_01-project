import unittest
from models import User, Restaurant, Points
from models import db
import time
from app import app
from helpers import points as pointshelper

class UpdatePointsTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_update_nonexistent_points_entry(self):
        points = Points(uid=1, rid=13, points=10)
        db.session.add(points)
        db.session.commit()
        errmsg = pointshelper.update_points(1, 12, 10)
        self.assertEqual(errmsg, ["Points entry does not exist for the given user ID and restaurant ID."])

    def test_update_points_entry_positive_increment(self):
        points = Points(uid=1, rid=12, points=10)
        db.session.add(points)
        db.session.commit()
        errmsg = pointshelper.update_points(1, 12, 10)
        self.assertEqual(errmsg, None)

        points = Points.query.filter_by(uid=1, rid=12).first()
        self.assertNotEqual(points, None)
        self.assertEqual(points.pid, 1)
        self.assertEqual(points.uid, 1)
        self.assertEqual(points.rid, 12)
        self.assertEqual(points.points, 20)

    def test_update_points_entry_zero_increment(self):
        points = Points(uid=1, rid=12, points=10)
        db.session.add(points)
        db.session.commit()
        errmsg = pointshelper.update_points(1, 12, 0)
        self.assertEqual(errmsg, None)

        points = Points.query.filter_by(uid=1, rid=12).first()
        self.assertNotEqual(points, None)
        self.assertEqual(points.pid, 1)
        self.assertEqual(points.uid, 1)
        self.assertEqual(points.rid, 12)
        self.assertEqual(points.points, 10)

    def test_update_points_entry_negative_increment_less_than_existing_points(self):
        points = Points(uid=1, rid=12, points=10)
        db.session.add(points)
        db.session.commit()
        errmsg = pointshelper.update_points(1, 12, -5)
        self.assertEqual(errmsg, None)

        points = Points.query.filter_by(uid=1, rid=12).first()
        self.assertNotEqual(points, None)
        self.assertEqual(points.pid, 1)
        self.assertEqual(points.uid, 1)
        self.assertEqual(points.rid, 12)
        self.assertEqual(points.points, 5)

    def test_update_points_entry_negative_increment_equal_to_existing_points(self):
        points = Points(uid=1, rid=12, points=10)
        db.session.add(points)
        db.session.commit()
        errmsg = pointshelper.update_points(1, 12, -10)
        self.assertEqual(errmsg, None)

        points = Points.query.filter_by(uid=1, rid=12).first()
        self.assertNotEqual(points, None)
        self.assertEqual(points.pid, 1)
        self.assertEqual(points.uid, 1)
        self.assertEqual(points.rid, 12)
        self.assertEqual(points.points, 0)

    def test_update_points_entry_negative_increment_greater_than_existing_points(self):
        points = Points(uid=1, rid=12, points=10)
        db.session.add(points)
        db.session.commit()
        errmsg = pointshelper.update_points(1, 12, -20)
        self.assertEqual(errmsg, ["A points entry cannot have a negative point count."])

        points = Points.query.filter_by(uid=1, rid=12).first()
        self.assertNotEqual(points, None)
        self.assertEqual(points.pid, 1)
        self.assertEqual(points.uid, 1)
        self.assertEqual(points.rid, 12)
        self.assertEqual(points.points, 10)


if __name__ == "__main__":
    unittest.main()

