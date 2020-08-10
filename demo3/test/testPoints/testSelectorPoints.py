import unittest
from models import User, Restaurant, Points
from models import db
import time
from app import app
from databaseHelpers import points as pointshelper

class SelectPointsTest(unittest.TestCase):
    """
    Test get_points() in databaseHelpers/points.py
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

    def test_get_existing_points_entry(self):
        """
        Test get a point entry by given valid input. Expect output to match correct data.
        """
        newEntry = Points(uid=1, rid=12, points=10)
        db.session.add(newEntry)
        db.session.commit()
        points = pointshelper.get_points(1, 12)
        self.assertNotEqual(points, None)
        self.assertEqual(points.pid, 1)
        self.assertEqual(points.uid, 1)
        self.assertEqual(points.rid, 12)
        self.assertEqual(points.points, 10)

    def test_get_nonexistent_points_entry(self):
        """
        Test get a point entry with invalid input. Expect return none.
        """
        newEntry = Points(uid=1, rid=13, points=10)
        db.session.add(newEntry)
        db.session.commit()
        points = pointshelper.get_points(2, 12)
        self.assertEqual(points, None)

    def test_get_nonexistent_points_entry_duplicate_uid(self):
        """
        Test get a point entry with invalid rid. Expect return none.
        """
        newEntry = Points(uid=1, rid=13, points=10)
        db.session.add(newEntry)
        db.session.commit()
        points = pointshelper.get_points(1, 12)
        self.assertEqual(points, None)

    def test_get_nonexistent_points_entry_duplicate_rid(self):
        """
        Test get a point entry with invalid uid. Expect return none.
        """
        newEntry = Points(uid=1, rid=13, points=10)
        db.session.add(newEntry)
        db.session.commit()
        points = pointshelper.get_points(2, 13)
        self.assertEqual(points, None)


if __name__ == "__main__":
    unittest.main()
