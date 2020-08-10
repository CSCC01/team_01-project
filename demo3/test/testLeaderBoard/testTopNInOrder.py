import unittest

from databaseHelpers.leaderboard import top_n_in_order
from models import User, Experience
from models import db
from app import app

class TopNInordertest(unittest.TestCase):
    """
    Test top_n_in_order() in databaseHelpers.coupon.py.
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

    def test_sort_fewer_than_n(self):
        """
        Test get a list of top N user in order with actual number of user is less than N, which is valid. Expect output to match correct data without any issues.
        """
        e1 = Experience(rid=1, uid=3, experience=100)
        e2 = Experience(rid=1, uid=1, experience=89)
        e3 = Experience(rid=1, uid=12, experience=1343)
        db.session.add(e1)
        db.session.add(e2)
        db.session.add(e3)
        db.session.commit()
        list = top_n_in_order(1,5)
        self.assertEqual([(12, 1343), (3, 100), (1, 89)], list)

    def test_sort_more_than_n(self):
        """
        Test get a list of top N user in order with actual number of user is larger than N, which is valid. Expect output to match correct data without any issues.
        """
        e1 = Experience(rid=1, uid=3, experience=100)
        e2 = Experience(rid=1, uid=1, experience=89)
        e3 = Experience(rid=1, uid=12, experience=1343)
        e4 = Experience(rid=1, uid=22, experience=1839)
        e5 = Experience(rid=1, uid=2, experience=20)
        db.session.add(e1)
        db.session.add(e2)
        db.session.add(e3)
        db.session.add(e4)
        db.session.add(e5)
        db.session.commit()
        list = top_n_in_order(1, 3)
        self.assertEqual([(22, 1839), (12, 1343), (3, 100)], list)


if __name__ == "__main__":
    unittest.main()

