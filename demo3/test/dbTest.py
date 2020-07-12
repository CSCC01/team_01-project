import unittest
from flask import Flask
from models import User, Coupon, Restaurant, Employee
import json
from models import db
import time
from app import app
import os


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_main_page_1(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_2(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_3(self):
        response = self.app.get('/login.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_append_data(self):
        u = User(name='nm', email='em', password='222')
        db.session.add(u)
        db.session.commit()
        user = User.query.filter_by(email='em').first()
        self.assertIsNotNone(user)
        # time.sleep(10)

    # Testing normal user code creation back-end(database insertion).
    # Creating a normal user code and test after inserting it to the
    # database by seeing if it stores correctly
    def test_owner_creation_normal_with_data(self):
        u = User(name="joe", password="passwd", email="joe@utsc.com", type=1)
        db.session.add(u)
        db.session.commit()
        # time.sleep(10)
        user = User.query.filter_by(email="joe@utsc.com").first()
        self.assertIsNotNone(user)
        self.assertGreater(user.uid, 0)
        self.assertEqual(user.name, "joe")
        self.assertEqual(user.password, "passwd")
        self.assertEqual(user.type, 1)

    def test_customer_creation_normal_with_data(self):
        u = User(name="George", password="passwd", email="george@utsc.com", type=-1)
        db.session.add(u)
        db.session.commit()
        # time.sleep(10)
        user = User.query.filter_by(email="george@utsc.com").first()
        self.assertIsNotNone(user)
        self.assertGreater(user.uid, 0)
        self.assertEqual(user.name, "George")
        self.assertEqual(user.password, "passwd")
        self.assertEqual(user.type, -1)

    def test_multi_customer_creation_normal_with_data(self):
        u1 = User(name="George", password="passwd", email="george@utsc.com", type=-1)
        db.session.add(u1)
        u2 = User(name="George", password="passwd", email="george2@utsc.com", type=-1)
        db.session.add(u2)
        db.session.commit()
        # time.sleep(10)
        user = User.query.filter_by(email="george@utsc.com").first()
        self.assertIsNotNone(user)
        self.assertGreater(user.uid, 0)
        self.assertEqual(user.name, "George")
        self.assertEqual(user.password, "passwd")
        self.assertEqual(user.type, -1)
        user2 = User.query.filter_by(email="george2@utsc.com").first()
        self.assertIsNotNone(user2)
        self.assertGreater(user.uid, 0)
        self.assertEqual(user.name, "George")
        self.assertEqual(user.password, "passwd")
        self.assertEqual(user.type, -1)

    def test_multi_customer_creation_same_email(self):
        # u1 = User(name="George", password="passwd", email="george@utsc.com", type=-1)
        # db.session.add(u1)
        # u2 = User(name="Wade", password="passwd", email="george@utsc.com", type=-1)
        # db.session.add(u2)
        # db.session.commit()
        # # time.sleep(10)
        # user = User.query.filter_by(email="george@utsc.com").first()
        # self.assertIsNotNone(user)
        # self.assertGreater(user.uid, 0)
        # self.assertEqual(user.name, "George")
        # self.assertEqual(user.password, "passwd")
        # self.assertEqual(user.type, -1)
        # user2 = User.query.filter_by(email="george@utsc.com").first()
        # self.assertIsNotNone(user2)
        # self.assertGreater(user.uid, 0)
        # self.assertEqual(user.name, "Wade")
        # self.assertEqual(user.password, "passwd")
        # self.assertEqual(user.type, -1)
        pass

    def test_user_normal(self):
        response = self.app.post("/registration2", data={'name': 'joe', 'email': 'joe@utsc.com', 'password': 'passwd',
                                                         'password2': 'passwd', 'address': 'address'})
        self.assertEqual('302 FOUND', response.status)

    def test_user_normal_miss_info_1(self):
        response = self.app.post("/registration2", data={'password': 'passwd',
                                                         'password2': 'passwd', 'address': 'address'})
        self.assertEqual('302 FOUND', response.status)

    def test_user_normal_miss_info_2(self):
        response = self.app.post("/registration2", data={'name': 'joe', 'email': 'joe@utsc.com',
                                                         'password2': 'passwd'})
        self.assertEqual('302 FOUND', response.status)


if __name__ == "__main__":
    unittest.main()
