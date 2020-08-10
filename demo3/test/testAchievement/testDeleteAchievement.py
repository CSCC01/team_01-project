import unittest
from app import app
from databaseHelpers.achievement import *
from models import db
from models import Achievements


class DeleteAchievementTest(unittest.TestCase):
    """
    Test function on deleting achievement
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

    def test_delete_one_achievement(self):
        """
        Test delete on one valid achievement
        """
        ac1 = Achievements(aid=32, rid=12, name='test', experience=10, points=10, type=1, value='test')
        ac2 = Achievements(aid=22, rid=12, name='test', experience=10, points=10, type=1, value='test')
        db.session.add(ac1)
        db.session.add(ac2)
        db.session.commit()
        errmsg = delete_achievement(32)
        a1 = Achievements.query.filter_by(aid=32).first()
        a2 = Achievements.query.filter_by(aid=22).first()
        self.assertEqual(errmsg, None)
        self.assertIsNone(a1)
        self.assertIsNotNone(a2)

    def test_delete_non_exist_achievement(self):
        """
        Test delete on a non-existing achievement
        """
        errmsg = delete_achievement(2)
        self.assertEqual(errmsg, "No such achievement")


if __name__ == "__main__":
    unittest.main()
