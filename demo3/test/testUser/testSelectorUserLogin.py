import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from databaseHelpers import user as userhelper

class SelectUserTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_one_user(self):
        user = User(name="joe", email="joe@utsc.com", password="passwd", type=-1)
        db.session.add(user)
        db.session.commit()
        u = userhelper.get_user_login("joe@utsc.com", "passwd")
        self.assertIsNotNone(u)
        self.assertEqual(u.name, "joe")
        self.assertEqual(u.email, "joe@utsc.com")
        self.assertEqual(u.password, "passwd")
        self.assertEqual(u.type, -1)

    def test_login_multi_user(self):
        user1 = User(name="joe", email="joe@utsc.com", password="passwd", type=-1)
        user2 = User(name="joseph", email="jsobe@utsc.com", password="passwd", type=1)
        user3 = User(name="sjoeb", email="sjoeb@utsc.com", password="passwd", type=0)
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()
        u = userhelper.get_user_login("jsobe@utsc.com", "passwd")
        self.assertIsNotNone(u)

    def test_login_wrong_password(self):
        user = User(name="joe", email="joe@utsc.com", password="passwd", type=-1)
        db.session.add(user)
        db.session.commit()
        u = userhelper.get_user_login("joe@utsc.com", "wrong_password")
        self.assertIsNone(u)



if __name__ == "__main__":
    unittest.main()
