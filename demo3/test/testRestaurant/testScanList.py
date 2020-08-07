import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from databaseHelpers import restaurant as rhelper

class SelectResNameTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testOneEmployee(self):
        r = Restaurant(rid=2, uid=17, name="", address="")
        e = Employee(uid=77, rid=2)
        db.session.add(r)
        db.session.add(e)
        db.session.commit()
        access = rhelper.verify_scan_list(2)
        self.assertEqual([17, 77], access)

    def testManyEmployee(self):
        r = Restaurant(rid=2, uid=17, name="", address="")
        e1 = Employee(uid=77, rid=2)
        e2 = Employee(uid=189, rid=2)
        e3 = Employee(uid=98, rid=3)
        db.session.add(r)
        db.session.add(e1)
        db.session.add(e2)
        db.session.add(e3)
        db.session.commit()
        access = rhelper.verify_scan_list(2)
        self.assertEqual([17, 77, 189], access)


if __name__ == "__main__":
    unittest.main()
