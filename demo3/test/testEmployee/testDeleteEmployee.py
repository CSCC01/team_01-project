import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from databaseHelpers import employee as employeehelper


class DeleteEmployeeTest(unittest.TestCase):
    """
    Test delete_employee() in databaseHelpers/employee.py
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

    def test_delete_one_employee(self):
        """
        Test delete an employee, check both user and employee database. Expect return none.
        """
        user = User(uid=9187, name="joe", email="joe.com", password="passwd", type=0)
        employee = Employee(uid=9187, rid=18)
        db.session.add(user)
        db.session.add(employee)
        db.session.commit()
        employeehelper.delete_employee(9187)
        e = Employee.query.filter_by(uid=9187).first()
        u = User.query.filter_by(uid=9187).first()
        self.assertIsNone(e)
        self.assertIsNone(u)



if __name__ == "__main__":
    unittest.main()
