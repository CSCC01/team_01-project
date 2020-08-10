import unittest
from app import app
from databaseHelpers.achievement import *
from models import db
from models import Achievements


class TestGetExistAid(unittest.TestCase):
    """
    Tests get_exist_aid() in databaseHelpers/achievement.py
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

    def test_get_exist_none(self):
        """
        Test getting a list of aid, but nothing is in achievement database(valid). Expect return none.
        """
        aid_list = get_exist_aid()
        self.assertEqual([], aid_list)

    def test_get_exist_one(self):
        """
        Test getting a list of aid with only one achievement in the database, which is only 1 aid(valid)
        """
        ac1 = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=1, value='test')
        db.session.add(ac1)
        db.session.commit()
        aid_list = get_exist_aid()
        self.assertEqual([32], aid_list)

    def test_get_exist_many(self):
        """
        Test getting a list of aid in database with more than one achievement in the database
        """
        ac1 = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=1, value='test')
        ac2 = Achievements(aid=22, rid=12, name='test', experience=10, points=10, type=1, value='test')
        ac3 = Achievements(aid=42, rid=52, name='test', experience=10, points=10, type=1, value='test')
        db.session.add(ac1)
        db.session.add(ac2)
        db.session.add(ac3)
        db.session.commit()
        aid_list = get_exist_aid()
        self.assertEqual([22, 32, 42], aid_list)


if __name__ == "__main__":
    unittest.main()