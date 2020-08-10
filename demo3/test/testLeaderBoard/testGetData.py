import unittest

from databaseHelpers.leaderboard import top_n_in_order, get_data
from models import User, Experience
from models import db
from app import app

class TopNInordertest(unittest.TestCase):
    """
    Test get_data() in databaseHelpers.coupon.py.
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

    def test_get_data(self):
        """
        Test get data from a list given by top_n_in_order()(top_n_in_order() should be test before this test). Expect output to match correct data.
        """
        e1 = Experience(rid=1, uid=3, experience=1000)
        e2 = Experience(rid=1, uid=1, experience=5000)
        u1 = User(uid=3, name="Joe", password="password", email="joe@utsc.com", type=-1)
        u2 = User(uid=1, name="Bob", password="password", email="bob@utsc.com", type=-1)
        db.session.add(e1)
        db.session.add(e2)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        list = top_n_in_order(1, 5)
        data = get_data(list)
        self.assertEqual([{"username": "Bob",
                           "exp": 5000,
                           "level": 9,
                           "rank": 1,
                           "uid": 1},
                          {"username": "Joe",
                           "exp": 1000,
                           "level": 4,
                           "rank": 2,
                           "uid": 3}], data)


if __name__ == "__main__":
    unittest.main()