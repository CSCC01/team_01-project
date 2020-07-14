import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from helpers import insertor


class InsertEmployeeTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_default_employee(self):
        insertor.insert_new_employee(12, 14)
        employee = Employee.query.filter_by(uid=12).first()
        self.assertIsNotNone(employee)

    def test_add_employees_one_res(self):
        insertor.insert_new_employee(12, 14)
        insertor.insert_new_employee(2, 14)
        insertor.insert_new_employee(18, 14)
        e1 = Employee.query.filter_by(uid=12).first()
        e2 = Employee.query.filter_by(uid=2).first()
        e3 = Employee.query.filter_by(uid=18).first()
        self.assertIsNotNone(e1)
        self.assertIsNotNone(e2)
        self.assertIsNotNone(e3)
        self.assertEqual(e1.rid, 14)
        self.assertEqual(e2.rid, 14)
        self.assertEqual(e3.rid, 14)

    def test_add_employees_multi_res(self):
        insertor.insert_new_employee(12, 12)
        insertor.insert_new_employee(2, 16)
        insertor.insert_new_employee(18, 4)
        e1 = Employee.query.filter_by(uid=12).first()
        e2 = Employee.query.filter_by(uid=2).first()
        e3 = Employee.query.filter_by(uid=18).first()
        self.assertIsNotNone(e1)
        self.assertIsNotNone(e2)
        self.assertIsNotNone(e3)
        self.assertEqual(e1.rid, 12)
        self.assertEqual(e2.rid, 16)
        self.assertEqual(e3.rid, 4)


if __name__ == "__main__":
    unittest.main()
