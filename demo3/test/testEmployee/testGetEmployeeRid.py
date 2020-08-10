import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from databaseHelpers.employee import *

class SelectEmployeeByRidTest(unittest.TestCase):
    """
    Test get_employee_rid() in employee.py
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

    def test_no_employee(self):
        """
        Test get a rid by given invalid uid. Expect return none.
        """
        e1 = Employee(uid=3, rid=7)
        e2 = Employee(uid=6, rid=9)
        db.session.add(e1)
        db.session.add(e2)
        db.session.commit()
        result = get_employee_rid(9)
        self.assertEqual(result, None)

    def test_employee(self):
        """
        Test get a rid by given valid employee uid. Expect output to match correct data.
        """
        e1 = Employee(uid=3, rid=7)
        e2 = Employee(uid=6, rid=9)
        db.session.add(e1)
        db.session.add(e2)
        db.session.commit()
        result = get_employee_rid(6)
        self.assertEqual(result, 9)

if __name__ == "__main__":
    unittest.main()
