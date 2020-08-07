import unittest
from app import app
from databaseHelpers.achievement import *
from models import db
from models import Achievements


class SelectAchievementTest(unittest.TestCase):
    """
    Tests the get_errmsg method in achievement.py.
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

    def test_no_errmsg(self):
        """Valid input, no error messages should be appeneded."""
        result = get_errmsg("Valid", '50', '25', '1', ";10.99;;;")
        actual = []
        self.assertEqual(result, actual)

    def test_empty_name(self):
        """Achievement is missing a name."""
        result = get_errmsg("", '50', '25', 1, ";10.99;;;")
        actual = ["Invalid achievement name, please provide an achievement name."]
        self.assertEqual(result, actual)

    def test_no_reward(self):
        """Achievement has no rewards, no points and no experience."""
        result = get_errmsg("Valid", '0', '0', 1, ";10.99;;;")
        actual = ["Missing experience and points, please provide at least one reward."]
        self.assertEqual(result, actual)

    def test_negative_points(self):
        """Achievement has negative points."""
        result = get_errmsg("Valid", '50', '-25', 1, ";10.99;;;")
        actual = ["Invalid points, please provide non-negative value."]
        self.assertEqual(result, actual)

    def test_negative_experience(self):
        """Achievement has negative experience."""
        result = get_errmsg("Valid", '-50', '25', 1, ";10.99;;;")
        actual = ["Invalid experience, please provide non-negative value."]
        self.assertEqual(result, actual)

    def test_type0_no_item(self):
        """A type 0 achievement has no item element."""
        result = get_errmsg("Valid", '50', '25', 0, ";10;;;")
        actual = ["Missing an item, please provide an item for the achievement."]
        self.assertEqual(result, actual)

    def test_negative_amount(self):
        """Achievement has a negative amount."""
        result = get_errmsg("Valid", '50', '25', 0, "coffee;-10;;;")
        actual = ["Invalid amount, please provide a positive value."]
        self.assertEqual(result, actual)

    def test_type3_definite_missing_beginging_date(self):
        """A type 3 definite achievement has no start date."""
        result = get_errmsg("Valid", '50', '25', 3, ";3;False;;2099-05-28")
        actual = ["Missing start or expiration date."]
        self.assertEqual(result, actual)

    def test_type3_definite_missing_end_date(self):
        """A type 3 definite achievement has no end date."""
        result = get_errmsg("Valid", '50', '25', 3, ";3;False;2020-05-28;")
        actual = ["Missing start or expiration date."]
        self.assertEqual(result, actual)

    def test_type3_definite_missing_dates(self):
        """A type 3 definite achievement is missing both a start and end date."""
        result = get_errmsg("Valid", '50', '25', 3, ";3;False;;")
        actual = ["Missing start or expiration date."]
        self.assertEqual(result, actual)

    def test_type3_definite_old_date(self):
        """A type 3 definite achievement is already expired."""
        result = get_errmsg("Valid", '50', '25', 3, ";3;False;2020-05-28;2020-06-9")
        actual = ["This achievemnt is already outdated."]
        self.assertEqual(result, actual)

    def test_definite_expi_early(self):
        """
        A definite achievement with expiration date is earlier than begin date. Expect an errmsg.
        """
        result = get_errmsg("Invalid", '50', '10', 1, ";3;False;2099-06-9;2099-06-8")
        actual = ["Invalid date interval, begin date must be before expiration date."]
        self.assertEqual(result, actual)

    def test_many_errmsg(self):
        """An achievement that violates multiple issues."""
        result = get_errmsg("", '-50', '-25', '2', ";-3;;;")
        actual = ["Invalid achievement name, please provide an achievement name.",
                    "Invalid experience, please provide non-negative value.",
                    "Invalid points, please provide non-negative value.",
                    "Invalid amount, please provide a positive value."]
        self.assertEqual(result, actual)


if __name__ == "__main__":
    unittest.main()
