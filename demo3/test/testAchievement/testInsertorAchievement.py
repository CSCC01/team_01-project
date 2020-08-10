import unittest
from models import Achievements
from models import db
import time
from app import app
from databaseHelpers.achievement import *


class InsertAchievementTest(unittest.TestCase):
    """
    Test insert_achievement() in databaseHelpers/achievement.py
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

    def test_insert_normal_zero_type(self):
        """
        Test insert a normal achievement of type 0.
        """
        insert_achievement(rid=8, name='Starbucks', experience=10, points=5, type=0, value = "coffee;3;False;2020-4-11;2020-12-31")
        a = Achievements.query.filter_by(rid=8).first()
        self.assertEqual(a.name, 'Starbucks')
        self.assertEqual(a.experience, 10)
        self.assertEqual(a.points, 5)
        self.assertEqual(a.type, 0)
        self.assertEqual(a.value, 'coffee;3;False;2020-4-11;2020-12-31')


    def test_insert_normal_one_type(self):
        """
        Test insert a normal achievement of type 1.
        """
        insert_achievement(rid=9, name='Starbucks', experience=10, points=5, type=1, value = ";4;False;2020-4-11;2020-12-31")
        a = Achievements.query.filter_by(rid=9).first()
        self.assertEqual(a.name, 'Starbucks')
        self.assertEqual(a.experience, 10)
        self.assertEqual(a.points, 5)
        self.assertEqual(a.type, 1)
        self.assertEqual(a.value, ';4;False;2020-4-11;2020-12-31')

    def test_insert_normal_one_type(self):
        """
        Test insert a normal achievement of type 2.
        """
        insert_achievement(rid=9, name='Starbucks', experience=10, points=5, type=2, value = ";3;False;2020-4-11;2020-12-31")
        a = Achievements.query.filter_by(rid=9).first()
        self.assertEqual(a.name, 'Starbucks')
        self.assertEqual(a.experience, 10)
        self.assertEqual(a.points, 5)
        self.assertEqual(a.type, 2)
        self.assertEqual(a.value, ';3;False;2020-4-11;2020-12-31')

    def test_insert_normal_one_type(self):
        """
        Test insert a normal achievement of type 3, definite date.
        """
        insert_achievement(rid=9, name='Starbucks', experience=10, points=5, type=3, value = ";5;False;2020-4-11;2020-12-31")
        a = Achievements.query.filter_by(rid=9).first()
        self.assertEqual(a.name, 'Starbucks')
        self.assertEqual(a.experience, 10)
        self.assertEqual(a.points, 5)
        self.assertEqual(a.type, 3)
        self.assertEqual(a.value, ";5;False;2020-4-11;2020-12-31")

    def test_insert_normal_one_type(self):
        """
        Test insert a normal achievement of type 3, indefinite date.
        """
        insert_achievement(rid=9, name='Starbucks', experience=10, points=5, type=3, value = ";4;True;;")
        a = Achievements.query.filter_by(rid=9).first()
        self.assertEqual(a.name, 'Starbucks')
        self.assertEqual(a.experience, 10)
        self.assertEqual(a.points, 5)
        self.assertEqual(a.type, 3)
        self.assertEqual(a.value, ';4;True;;')


if __name__ == "__main__":
    unittest.main()
