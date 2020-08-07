"""

Test suite for helper.coupon.py's insert_coupon function.

"""


import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from databaseHelpers import coupon as couponhelper
import datetime

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
        """
        Inserts a valid coupon with a given begining and expiration date.
        """
        begin = datetime.date(2020, 5, 1)
        end = datetime.date(2020, 6, 30)
        errmsg = couponhelper.insert_coupon(12, "name", 100, "50% off", 2, begin, end, False)
        coupon = Coupon.query.filter_by(rid=12, name="name").first()
        self.assertIsNotNone(coupon)
        self.assertEqual(coupon.cid, 1)
        self.assertEqual(coupon.rid, 12)
        self.assertEqual(coupon.name, "name")
        self.assertEqual(coupon.points, 100)
        self.assertEqual(coupon.description, "50% off")
        self.assertEqual(coupon.level, 2)
        self.assertEqual(coupon.begin, begin)
        self.assertEqual(coupon.expiration, end)
        self.assertEqual(coupon.deleted, 0)
        self.assertEqual(errmsg, None)

    def test_insert_default_indefinite_coupon(self):
        """
        Inserts a valid coupon with out a set beginning/expiration date.
        """
        errmsg = couponhelper.insert_coupon(15, "indefinite", 200, "10% off", 3, None, None, True)
        coupon = Coupon.query.filter_by(rid=15, name="indefinite").first()
        self.assertIsNotNone(coupon)
        self.assertEqual(coupon.cid, 1)
        self.assertEqual(coupon.rid, 15)
        self.assertEqual(coupon.name, "indefinite")
        self.assertEqual(coupon.points, 200)
        self.assertEqual(coupon.description, "10% off")
        self.assertEqual(coupon.level, 3)
        self.assertEqual(coupon.deleted, 0)
        self.assertEqual(errmsg, None)

    def test_insert_multi_coupons(self):
        """
        Inserts multiple valid coupons.
        """
        begin1 = datetime.date(2020, 6, 2)
        end1 = datetime.date(2020, 8, 2)
        begin2 = datetime.date(2020, 5, 1)
        end2 = datetime.date(2020, 6, 30)
        errmsg1 = couponhelper.insert_coupon(12, "one", 100, "50% off", 1, begin1, end1, False)
        errmsg2 = couponhelper.insert_coupon(12, "two", 300, "70% off", 2, begin2, end2, False)
        errmsg3 = couponhelper.insert_coupon(12, "three", 1000, "100% off", 3, None, None, True)
        self.assertEqual(errmsg1, None)
        self.assertEqual(errmsg2, None)
        self.assertEqual(errmsg3, None)

    def test_insert_invalid_points_negative(self):
        """
        Tries to insert an invalid coupon with an invalid amount of points (negative). Expects an error message.
        """
        begin = datetime.date(2020, 5, 1)
        end = datetime.date(2020, 6, 30)
        errmsg = couponhelper.insert_coupon(2, "one", -100, "50% off", 1, begin, end, False)
        self.assertEqual(errmsg, ["Invalid amount for points."])

    def test_insert_invalid_points_empty(self):
        """
        Tries to insert an invalid coupon with an invalid amount of points (none). Expects an error message.
        """
        begin = datetime.date(2020, 5, 1)
        end = datetime.date(2020, 6, 30)
        errmsg = couponhelper.insert_coupon(2, "one", "", "50% off", 1, begin, end, False)
        self.assertEqual(errmsg, ["Invalid amount for points."])

    def test_insert_invalid_name_empty(self):
        """
        Tries to insert an invalid coupon with an invalid name (none). Expects an error message.
        """
        errmsg = couponhelper.insert_coupon(4, "", 100, "30% off", 2, None, None, True)
        self.assertEqual(errmsg, ["Invalid coupon name, please give your coupon a name."])

    def test_insert_invalid_date_both(self):
        """
        Tries to insert an invalid coupon with an invalid date (none). Expects an error message.
        """
        errmsg = couponhelper.insert_coupon(4, "name", 100, "30% off", 3, None, None, False)
        self.assertEqual(errmsg, ["Missing start or expiration date."])

    def test_insert_invalid_date_begin(self):
        """
        Tries to insert an invalid coupon with an invalid beginning date (none). Expects an error message.
        """
        end = datetime.date(2020, 6, 30)
        errmsg = couponhelper.insert_coupon(4, "name", 100, "30% off", 1, None, end, False)
        self.assertEqual(errmsg, ["Missing start or expiration date."])

    def test_insert_invalid_date_end(self):
        """
        Tries to insert an invalid coupon with an invalid expiration date (none). Expects an error message.
        """
        begin = datetime.date(2020, 6, 30)
        errmsg = couponhelper.insert_coupon(4, "name", 100, "30% off", 2, begin, None, False)
        self.assertEqual(errmsg, ["Missing start or expiration date."])

    def test_insert_invalid_date_expired_early(self):
        """
        Tries to insert an invalid coupon with an invalid expiration date which earlier than begin date. Expect an error message.
        """
        begin = datetime.date(2020, 6, 30)
        end = datetime.date(2020, 5, 31)
        errmsg = couponhelper.insert_coupon(4, "name", 100, "30% off", 2, begin, end, False)
        self.assertEqual(errmsg, ["Invalid date interval, begin date must be before expiration date."])

    def test_insert_invalid_level_negative(self):
        """
        Tries to insert an invalid coupon with an invalid amount of level (negative). Expects an error message.
        """
        begin = datetime.date(2020, 5, 1)
        end = datetime.date(2020, 6, 30)
        errmsg = couponhelper.insert_coupon(2, "one", 10, "50% off", -10, begin, end, False)
        self.assertEqual(errmsg, ["Invalid level requirement, please give a non-negative value."])

    def test_insert_invalid_level_empty(self):
        """
        Tries to insert an invalid coupon with an invalid input of level, which is empty. Expects an error message.
        """
        begin = datetime.date(2020, 5, 1)
        end = datetime.date(2020, 6, 30)
        errmsg = couponhelper.insert_coupon(2, "one", 10, "50% off", "", begin, end, False)
        self.assertEqual(errmsg, ["Invalid level requirement, please give a non-negative value."])

    def test_insert_invalid_name_date(self):
        """
        Tries to insert an invalid coupon with an invalid name (none) and dates (none). Expects an error message.
        """
        errmsg = couponhelper.insert_coupon(4, "", 100, "30% off", 3, None, None, False)
        self.assertEqual(errmsg,
                         ["Invalid coupon name, please give your coupon a name.", "Missing start or expiration date."])

    def test_insert_invalid_name_date_expi_early(self):
        """
        Tries to insert an invalid coupon with an invalid name (none) and dates (none). Expects an error message.
        """
        begin = datetime.date(2020, 6, 30)
        end = datetime.date(2020, 5, 31)
        errmsg = couponhelper.insert_coupon(4, "", 100, "30% off", 3, begin, end, False)
        self.assertEqual(errmsg,
                         ["Invalid coupon name, please give your coupon a name.", "Invalid date interval, begin date must be before expiration date."])

    def test_insert_invalid_name_point(self):
        """
        Tries to insert an invalid coupon with an invalid name (none) and amount of points (none). Expects an error message.
        """
        errmsg = couponhelper.insert_coupon(4, "", "", "30% off", 2, None, None, True)
        self.assertEqual(errmsg,
                         ["Invalid amount for points.", "Invalid coupon name, please give your coupon a name."])
    
    def test_insert_invalid_name_level(self):
        """
        Tries to insert an invalid coupon with an invalid name (none) and invalid level (none). Expects an error message.
        """
        errmsg = couponhelper.insert_coupon(4, "", 100, "30% off", "", None, None, True)
        self.assertEqual(errmsg,
                         ["Invalid coupon name, please give your coupon a name.", "Invalid level requirement, please give a non-negative value."])

    def test_insert_invalid_point_date(self):
        """
        Tries to insert an invalid coupon with an invalid dates (none) and amount of points (negative). Expects an error message.
        """
        errmsg = couponhelper.insert_coupon(4, "name", -1, "30% off", 5, None, None, False)
        self.assertEqual(errmsg,
                         ["Invalid amount for points.", "Missing start or expiration date."])
    
    def test_insert_invalid_point_date_expi_early(self):
        """
        Tries to insert an invalid coupon with an invalid dates (expire early) and amount of points (negative). Expects an error message.
        """
        begin = datetime.date(2020, 6, 30)
        end = datetime.date(2020, 5, 31)
        errmsg = couponhelper.insert_coupon(4, "name", -1, "30% off", 5, begin, end, False)
        self.assertEqual(errmsg,
                         ["Invalid amount for points.", "Invalid date interval, begin date must be before expiration date."])

    def test_insert_invalid_point_level(self):
        """
        Tries to insert an invalid coupon with an invalid points (none) and invalid level (negative). Expects an error message.
        """
        errmsg = couponhelper.insert_coupon(4, "name", "", "30% off", -1, None, None, True)
        self.assertEqual(errmsg,
                         ["Invalid amount for points.", "Invalid level requirement, please give a non-negative value."])

    def test_insert_invalid_date_level(self):
        """
        Tries to insert an invalid coupon with an invalid date (none) and invalid level (none). Expects an error message.
        """
        errmsg = couponhelper.insert_coupon(4, "name", 12, "30% off", "", None, None, False)
        self.assertEqual(errmsg,
                         ["Invalid level requirement, please give a non-negative value.", "Missing start or expiration date."])

    def test_insert_invalid_date_level_expi_early(self):
        """
        Tries to insert an invalid coupon with an invalid date (expire early) and invalid level (none). Expects an error message.
        """
        begin = datetime.date(2020, 6, 30)
        end = datetime.date(2020, 5, 31)
        errmsg = couponhelper.insert_coupon(4, "name", 12, "30% off", "", begin, end, False)
        self.assertEqual(errmsg,
                         ["Invalid level requirement, please give a non-negative value.", "Invalid date interval, begin date must be before expiration date."])

    def test_insert_invalid_name_point_date(self):
        """
        Tries to insert an invalid coupon with an invalid dates (none), amount of points (negative) and name (none). Expects an error message.
        """
        errmsg = couponhelper.insert_coupon(4, "", -1, "30% off", 9, None, None, False)
        self.assertEqual(errmsg,
                         ["Invalid amount for points.", "Invalid coupon name, please give your coupon a name.",
                          "Missing start or expiration date."])
    
    def test_insert_invalid_name_point_date_expi_early(self):
        """
        Tries to insert an invalid coupon with an invalid dates (expire early), amount of points (negative) and name (none). Expects an error message.
        """
        begin = datetime.date(2020, 6, 30)
        end = datetime.date(2020, 5, 31)
        errmsg = couponhelper.insert_coupon(4, "", -1, "30% off", 9, begin, end, False)
        self.assertEqual(errmsg,
                         ["Invalid amount for points.", "Invalid coupon name, please give your coupon a name.",
                          "Invalid date interval, begin date must be before expiration date."])
    
    def test_insert_invalid_point_level_date(self):
        """
        Tries to insert an invalid coupon with an invalid dates (none), amount of points (negative) and level (none). Expects an error message.
        """
        errmsg = couponhelper.insert_coupon(4, "name", -1, "30% off", "", None, None, False)
        self.assertEqual(errmsg,
                         ["Invalid amount for points.", "Invalid level requirement, please give a non-negative value.",
                          "Missing start or expiration date."])
    
    def test_insert_invalid_point_level_date_expi_early(self):
        """
        Tries to insert an invalid coupon with an invalid dates (expire early), amount of points (negative) and level (none). Expects an error message.
        """
        begin = datetime.date(2020, 6, 30)
        end = datetime.date(2020, 5, 31)
        errmsg = couponhelper.insert_coupon(4, "name", -1, "30% off", "", begin, end, False)
        self.assertEqual(errmsg,
                         ["Invalid amount for points.", "Invalid level requirement, please give a non-negative value.",
                          "Invalid date interval, begin date must be before expiration date."])

    def test_insert_invalid_name_level_date(self):
        """
        Tries to insert an invalid coupon with an invalid dates (none), name (none) and level (negative). Expects an error message.
        """
        errmsg = couponhelper.insert_coupon(4, "", 1, "30% off", -5, None, None, False)
        self.assertEqual(errmsg,
                         ["Invalid coupon name, please give your coupon a name.", "Invalid level requirement, please give a non-negative value.",
                         "Missing start or expiration date."])

    def test_insert_invalid_name_level_date_expi_early(self):
        """
        Tries to insert an invalid coupon with an invalid dates (expire early), name (none) and level (negative). Expects an error message.
        """
        begin = datetime.date(2020, 6, 30)
        end = datetime.date(2020, 5, 31)
        errmsg = couponhelper.insert_coupon(4, "", 1, "30% off", -5, begin, end, False)
        self.assertEqual(errmsg,
                         ["Invalid coupon name, please give your coupon a name.", "Invalid level requirement, please give a non-negative value.",
                         "Invalid date interval, begin date must be before expiration date."])

    def test_insert_invalid_name_points_level(self):
        """
        Tries to insert an invalid coupon with an invalid points (negative), name (none) and level (none). Expects an error message.
        """
        errmsg = couponhelper.insert_coupon(4, "", -1, "30% off", "", None, None, True)
        self.assertEqual(errmsg,
                         ["Invalid amount for points.", "Invalid coupon name, please give your coupon a name.",
                         "Invalid level requirement, please give a non-negative value."])

    def test_insert_invalid_name_points_level_date(self):
        """
        Tries to insert and invalid coupon with all invalid, including name (none), points (negative), level (negative) and date (none). Expects an errmsg.
        """
        errmsg = couponhelper.insert_coupon(4, "", -1, "30% off", "", None, None, False)
        self.assertEqual(errmsg,
                         ["Invalid amount for points.", "Invalid coupon name, please give your coupon a name.",
                         "Invalid level requirement, please give a non-negative value.", "Missing start or expiration date."])

    def test_insert_invalid_name_points_level_date_expi_early(self):
        """
        Tries to insert and invalid coupon with all invalid, including name (none), points (negative), level (negative) and the expiration date is earlier than begin date. Expects an errmsg.
        """
        begin = datetime.date(2020, 6, 30)
        end = datetime.date(2020, 5, 31)
        errmsg = couponhelper.insert_coupon(4, "", -1, "30% off", "", begin, end, False)
        self.assertEqual(errmsg,
                         ["Invalid amount for points.", "Invalid coupon name, please give your coupon a name.",
                         "Invalid level requirement, please give a non-negative value.", "Invalid date interval, begin date must be before expiration date."])


if __name__ == "__main__":
    unittest.main()
