import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from databaseHelpers import employee as employeehelper

class SelectEmployeeTest(unittest.TestCase):
    """
    Test get_employees() in databaseHelpers/employee.py
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

    def test_employee_single(self):
        """
        Test valid retriving a list of employee which has only one employee.
        """
        e = Employee(uid=3, rid=7)
        u = User(uid=3, name="joe", email="joe.com", password="omit", type=0)
        db.session.add(e)
        db.session.add(u)
        db.session.commit()
        employee_list = employeehelper.get_employees(7)
        self.assertEqual(employee_list, [{'email': 'joe.com', 'name': 'joe', 'uid': 3, 'type': 0}])

    def test_employee_many(self):
        """
        Test valid retriving a list of employees.
        """
        e1 = Employee(uid=1, rid=7)
        e2 = Employee(uid=2, rid=7)
        e3 = Employee(uid=3, rid=7)
        u1 = User(name="joe", email="joe.com", password="omit", type=0)
        u2 = User(name="joetwo", email="joetwo.com", password="omit", type=2)
        u3 = User(name="joethree", email="joethree.com", password="omit", type=0)
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(e1)
        db.session.add(e2)
        db.session.add(e3)
        db.session.commit()
        employee_list = employeehelper.get_employees(7)
        self.assertEqual(employee_list, [
                    {'email': 'joe.com', 'name': 'joe', 'uid': 1, 'type': 0},
                    {'email': 'joetwo.com', 'name': 'joetwo', 'uid': 2, 'type': 2},
                    {'email': 'joethree.com', 'name': 'joethree', 'uid': 3, 'type': 0}])

    def test_employee_none(self):
        """
        Test retriving a list of employee but there is no employee in such restaurant with the rid. Expect return none.
        """
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
