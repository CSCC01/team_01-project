from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from app import app
from exts import db
from models import User
from models import Restaurant
from models import Employee
import config
import os
import unittest


class EmployeeDBTest(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.testing = True
        self.app = Flask(__name__)
        db.init_app(self.app)
        app.config['WTF_CSRF_ENABLED'] = False
        with app.app_context():
            db.create_all()
        pass
    # executed after each test
    def tearDown(self):
        db.session.remove()
        with app.app_context():
            db.drop_all()
        pass

    def test_add_default_employee(self):
        user = User(name='name', email='email', password='123', type=0)
        restaurant = Restaurant(name='name', address='address')
        with app.app_context():
            db.session.add(user)
            db.session.add(restaurant)
            db.session.commit()
            self.assertIsNotNone(User.query.filter_by(email='email').first())

            employee = Employee(uid = user.uid, rid = restaurant.rid)
            db.session.add(employee)
            db.session.commit()
            self.assertIsNotNone(Employee.query.filter_by(uid=user.uid).first())


    def test_add_employee_with_existing_employee_of_same_name(self):
        user = User(name='name', email='email', password='123', type=0)
        user2 = User(name='name', email='email2', password='123', type=0)
        with app.app_context():
            db.session.add(user)
            db.session.add(user2)
            db.session.commit()
            self.assertIsNotNone(User.query.filter_by(email='email2').first())
    
    def test_add_employee_with_existing_customer_of_same_name(self):
        user = User(name='name', email='email', password='123', type=-1)
        user2 = User(name='name', email='email2', password='123', type=0)
        with app.app_context():
            db.session.add(user)
            db.session.add(user2)
            db.session.commit()
            self.assertIsNotNone(User.query.filter_by(email='email2').first())

    def test_add_employee_with_existing_owner_of_same_name(self):
        user = User(name='name', email='email', password='123', type=1)
        user2 = User(name='name', email='email2', password='123', type=0)
        with app.app_context():
            db.session.add(user)
            db.session.add(user2)
            db.session.commit()
            self.assertIsNotNone(User.query.filter_by(email='email2').first())

    def test_add_employee_with_existing_employee_of_same_email(self):
        user = User(name='name', email='email', password='123', type=0)
        user2 = User(name='name2', email='email', password='123', type=0)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            db.session.add(user2)
            
            with self.assertRaises(IntegrityError):
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise
            self.assertEqual(1, User.query.filter_by(email='email').count())
    
    def test_add_employee_with_existing_customer_of_same_email(self):
        user = User(name='name', email='email', password='123', type=-1)
        user2 = User(name='name2', email='email', password='123', type=0)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            db.session.add(user2)
            
            with self.assertRaises(IntegrityError):
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise
            self.assertEqual(1, User.query.filter_by(email='email').count())

    def test_add_employee_with_existing_owner_of_same_email(self):
        user = User(name='name', email='email', password='123', type=1)
        user2 = User(name='name2', email='email', password='123', type=0)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            db.session.add(user2)
            
            with self.assertRaises(IntegrityError):
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise
            self.assertEqual(1, User.query.filter_by(email='email').count())

    if __name__ == "__main__":
        unittest.main()
