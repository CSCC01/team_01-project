import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from helpers import coupon as couponhelper
from datetime import datetime

class InsertCouponTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_insert_default_definite_coupon(self):
        begin = datetime.strptime("2 June, 2020", "%d %B, %Y")
        end = datetime.strptime("2 August, 2020", "%d %B, %Y")
        errmsg = couponhelper.insert_coupon(12, "name", 100, "50% off", begin, end, False)
        coupon = Coupon.query.filter_by(rid=12, name="name").first()
        self.assertIsNotNone(coupon)
        self.assertEqual(coupon.cid, 1)
        self.assertEqual(coupon.rid, 12)
        self.assertEqual(coupon.name, "name")
        self.assertEqual(coupon.points, 100)
        self.assertEqual(coupon.description, "50% off")
        self.assertEqual(coupon.begin, begin)
        self.assertEqual(coupon.expiration, end)
        self.assertEqual(coupon.deleted, 0)
        self.assertEqual(errmsg, None)

    def test_insert_default_indefinite_coupon(self):
        errmsg = couponhelper.insert_coupon(15, "indefinite", 200, "10% off", None, None, True)
        coupon = Coupon.query.filter_by(rid=15, name="indefinite").first()
        self.assertIsNotNone(coupon)
        self.assertEqual(coupon.cid, 1)
        self.assertEqual(coupon.rid, 15)
        self.assertEqual(coupon.name, "indefinite")
        self.assertEqual(coupon.points, 200)
        self.assertEqual(coupon.description, "10% off")
        self.assertEqual(coupon.deleted, 0)
        self.assertEqual(errmsg, None)

    def test_insert_multi_coupons(self):
        begin1 = datetime.strptime("2 June, 2020", "%d %B, %Y")
        end1 = datetime.strptime("2 August, 2020", "%d %B, %Y")
        begin2 = datetime.strptime("1 May, 2020", "%d %B, %Y")
        end2 = datetime.strptime("30 June, 2020", "%d %B, %Y")
        errmsg1 = couponhelper.insert_coupon(12, "one", 100, "50% off", begin1, end1, False)
        errmsg2 = couponhelper.insert_coupon(12, "two", 300, "70% off", begin2, end2, False)
        errmsg3 = couponhelper.insert_coupon(12, "three", 1000, "100% off", None, None, True)
        self.assertEqual(errmsg1, None)
        self.assertEqual(errmsg2, None)
        self.assertEqual(errmsg3, None)

    def test_insert_invalid_points_negative(self):
        begin = datetime.strptime("1 May, 2020", "%d %B, %Y")
        end = datetime.strptime("30 June, 2020", "%d %B, %Y")
        errmsg = couponhelper.insert_coupon(2, "one", -100, "50% off", begin, end, False)
        self.assertEqual(errmsg, ["Invalid amount for points."])

    def test_insert_invalid_points_empty(self):
        begin = datetime.strptime("1 May, 2020", "%d %B, %Y")
        end = datetime.strptime("30 June, 2020", "%d %B, %Y")
        errmsg = couponhelper.insert_coupon(2, "one", "", "50% off", begin, end, False)
        self.assertEqual(errmsg, ["Invalid amount for points."])

    def test_insert_invalid_name_empty(self):
        errmsg = couponhelper.insert_coupon(4, "", 100, "30% off", None, None, True)
        self.assertEqual(errmsg, ["Invalid coupon name, please give your coupon a name."])

    def test_insert_invalid_date_both(self):
        errmsg = couponhelper.insert_coupon(4, "name", 100, "30% off", None, None, False)
        self.assertEqual(errmsg, ["Missing start or expiration date."])

    def test_insert_invalid_date_begin(self):
        end = datetime.strptime("30 June, 2020", "%d %B, %Y")
        errmsg = couponhelper.insert_coupon(4, "name", 100, "30% off", None, end, False)
        self.assertEqual(errmsg, ["Missing start or expiration date."])

    def test_insert_invalid_date_end(self):
        begin = datetime.strptime("30 June, 2020", "%d %B, %Y")
        errmsg = couponhelper.insert_coupon(4, "name", 100, "30% off", begin, None, False)
        self.assertEqual(errmsg, ["Missing start or expiration date."])

    def test_insert_invalid_name_date(self):
        errmsg = couponhelper.insert_coupon(4, "", 100, "30% off", None, None, False)
        self.assertEqual(errmsg,
                         ["Invalid coupon name, please give your coupon a name.", "Missing start or expiration date."])

    def test_insert_invalid_name_point(self):
        errmsg = couponhelper.insert_coupon(4, "", "", "30% off", None, None, True)
        self.assertEqual(errmsg,
                         ["Invalid amount for points.", "Invalid coupon name, please give your coupon a name."])

    def test_insert_invalid_point_date(self):
        errmsg = couponhelper.insert_coupon(4, "name", -1, "30% off", None, None, False)
        self.assertEqual(errmsg,
                         ["Invalid amount for points.", "Missing start or expiration date."])

    def test_insert_invalid_name_point_date(self):
        errmsg = couponhelper.insert_coupon(4, "", -1, "30% off", None, None, False)
        self.assertEqual(errmsg,
                         ["Invalid amount for points.", "Invalid coupon name, please give your coupon a name.",
                          "Missing start or expiration date."])




if __name__ == "__main__":
    unittest.main()
