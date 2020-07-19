import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from helpers import employee as employeehelper

class SelectEmployeeTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_employee_single(self):
        e = Employee(uid=3, rid=7)
        u = User(uid=3, name="joe", email="joe.com", password="omit", type=0)
        db.session.add(e)
        db.session.add(u)
        db.session.commit()
        employee_list = employeehelper.get_employees(7)
        self.assertEqual(employee_list, [{'email': 'joe.com', 'name': 'joe', 'uid': 3}])

    def test_employee_many(self):
        e1 = Employee(uid=1, rid=7)
        e2 = Employee(uid=2, rid=7)
        e3 = Employee(uid=3, rid=7)
        u1 = User(name="joe", email="joe.com", password="omit", type=0)
        u2 = User(name="joetwo", email="joetwo.com", password="omit", type=0)
        u3 = User(name="joethree", email="joethree.com", password="omit", type=0)
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(e1)
        db.session.add(e2)
        db.session.add(e3)
        db.session.commit()
        employee_list = employeehelper.get_employees(7)
        self.assertEqual(employee_list, [{'email': 'joe.com', 'name': 'joe', 'uid': 1},
                    {'email': 'joetwo.com', 'name': 'joetwo', 'uid': 2},
                    {'email': 'joethree.com', 'name': 'joethree', 'uid': 3}])

    def test_employee_none(self):
        e1 = Employee(uid=1, rid=7)
        e2 = Employee(uid=2, rid=7)
        e3 = Employee(uid=3, rid=7)
        u1 = User(name="joe", email="joe.com", password="omit", type=0)
        u2 = User(name="joetwo", email="joetwo.com", password="omit", type=0)
        u3 = User(name="joethree", email="joethree.com", password="omit", type=0)
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(e1)
        db.session.add(e2)
        db.session.add(e3)
        db.session.commit()
        employee_list = employeehelper.get_employees(5)
        self.assertEqual(employee_list, [])



if __name__ == "__main__":
    unittest.main()
