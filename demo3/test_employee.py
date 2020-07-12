from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
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
        with app.app_context():
            user = self.add_user('name', 'email', '123', 0)
            restaurant = self.add_restaurant('name', 'address')
            employee = self.link_employee(user.uid, restaurant.rid)
            db.session.commit()
            self.assertIsNotNone(User.query.filter_by(email='email').first())
            self.assertIsNotNone(Employee.query.filter_by(uid=user.uid).first())

    def test_add_employee_with_existing_employee_of_same_name(self):
        with app.app_context():
            user = self.add_user('name', 'email', '123', 0)
            user2 = self.add_user('name', 'email2', '123', 0)
            db.session.commit()
            self.assertIsNotNone(User.query.filter_by(email='email2').first())
    
    def test_add_employee_with_existing_customer_of_same_name(self):
        with app.app_context():
            user = self.add_user('name', 'email', '123', -1)
            user2 = self.add_user('name', 'email2', '123', 0)
            db.session.commit()
            self.assertIsNotNone(User.query.filter_by(email='email2').first())

    def test_add_employee_with_existing_owner_of_same_name(self):
        with app.app_context():
            user = self.add_user('name', 'email', '123', 1)
            user2 = self.add_user('name', 'email2', '123', 0)
            db.session.commit()
            self.assertIsNotNone(User.query.filter_by(email='email2').first())

    def test_add_employee_with_existing_employee_of_same_email(self):
        with app.app_context():
            user = self.add_user('name','email', '123', 0)
            db.session.commit()
            user2 = self.add_user('name2', 'email', '123', 0)
            with self.assertRaises(IntegrityError):
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise
            self.assertEqual(1, User.query.filter_by(email='email').count())
    
    def test_add_employee_with_existing_customer_of_same_email(self):
        with app.app_context():
            user = self.add_user('name','email', '123', -1)
            db.session.commit()
            user2 = self.add_user('name2', 'email', '123', 0)
            with self.assertRaises(IntegrityError):
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise
            self.assertEqual(1, User.query.filter_by(email='email').count())

    def test_add_employee_with_existing_owner_of_same_email(self):
        with app.app_context():
            user = self.add_user('name','email', '123', 1)
            db.session.commit()
            user2 = self.add_user('name2', 'email', '123', 0)
            with self.assertRaises(IntegrityError):
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise
            self.assertEqual(1, User.query.filter_by(email='email').count())

    def test_link_multiple_employees_to_restaurant(self):
        with app.app_context():
            user = self.add_user('name', 'email', '123', 0)
            user2 = self.add_user('name2', 'email2', '123', 0)
            restaurant = self.add_restaurant('name', 'address')
            db.session.commit()
            
            employee = self.link_employee(user.uid, restaurant.rid)
            employee2 = self.link_employee(user2.uid, restaurant.rid)
            db.session.commit()

            self.assertEqual(2, Employee.query.filter_by(rid=restaurant.rid).count())

    def test_link_employee_to_multiple_restaurants(self):
        with app.app_context():
            user = self.add_user('name', 'email', '123', 0)
            restaurant = self.add_restaurant('name', 'address')
            restaurant2 = self.add_restaurant('name2', 'address2')
            employee = self.link_employee(user.uid, restaurant.rid)
            db.session.commit()

            employee2 = self.link_employee(user.uid, restaurant2.rid)
            with self.assertRaises(FlushError):
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise
            self.assertEqual(1, Employee.query.filter_by(uid=user.uid).count())

    # Helper functions
    def add_user(self, name, email, password, type):
        user = User(name=name, email=email, password=password, type=type)
        db.session.add(user)
        return user

    def add_restaurant(self, name, address):
        restaurant = Restaurant(name=name, address=address)
        db.session.add(restaurant)
        return restaurant

    def link_employee(self, uid, rid):
        employee = Employee(uid = uid, rid = rid)
        db.session.add(employee)
        return employee

    if __name__ == "__main__":
        unittest.main()
