import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import time
from app import app
from databaseHelpers import user as userhelper


class InsertUserTest(unittest.TestCase):
    '''
    Tests insert_new_user() in databaseHelpers/user.py.
    '''
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_insert_user_full_info(self):
        """
        Test insert a normal user account with full info. Expect output to match correct data.
        """
        userhelper.insert_new_user("joe", "joe@utsc.com", "passwd", "passwd", "-1")
        user = User.query.filter_by(email="joe@utsc.com").first()
        self.assertIsNotNone(user)
        self.assertGreater(user.uid, 0)
        self.assertEqual(user.name, "joe")
        self.assertEqual(user.password, "passwd")
        self.assertEqual(user.type, -1)

    def test_insert_user_same_email(self):
        """
        Test insert an invalid user account with an email that already exist in the database. Expect an error message.
        """
        userhelper.insert_new_user("joe", "joe@utsc.com", "passwd", "passwd", "-1")
        user = User.query.filter_by(email="joe@utsc.com").first()
        self.assertIsNotNone(user)
        errmsg = userhelper.insert_new_user("joseph", "joe@utsc.com", "passwd", "passwd", "1")
        self.assertEqual(errmsg, (["Email has already been used."], None))

    def test_insert_user_diff_password(self):
        """
        Test insert an invalid user with second password checking differs from the first password input. Expect an error message. 
        """
        errmsg = userhelper.insert_new_user("joe", "joe@utsc.com", "passwd", "dwssap", "-1")
        user = User.query.filter_by(email="joe@utsc.com").first()
        # to show that insert failed
        self.assertIsNone(user)
        self.assertEqual(errmsg, (["Passwords do not match."], None))

    def test_insert_user_miss_key_email(self):
        """
        Test insert an invalid user with missing email input. Expect an error message.
        """
        errmsg = userhelper.insert_new_user("joe", "", "passwd", "passwd", "-1")
        user = User.query.filter_by(name="joe").first()
        # to show that insert failed
        self.assertIsNone(user)
        self.assertEqual(errmsg, (["An email is required."], None))

    def test_insert_user_miss_key_password(self):
        """
        Test insert an invalid user with missing password input. Expect an error message.
        """
        errmsg = userhelper.insert_new_user("joe", "joe@utsc.com", "", "", "-1")
        user = User.query.filter_by(email="joe@utsc.com").first()
        # to show that insert failed
        self.assertIsNone(user)
        self.assertEqual(errmsg, (["A password is required."], None))

    def test_insert_user_miss_email_password(self):
        """
        Test insert an invalid user with both password and email are missing. Expect an error message.
        """
        # miss email and password
        errmsg = userhelper.insert_new_user("joe", "", "", "", "-1")
        user = User.query.filter_by(name="joe").first()
        # to show that insert failed
        self.assertIsNone(user)
        self.assertEqual(errmsg, (["An email is required.", "A password is required."], None))

    def test_insert_user_miss_email_wrong_password(self):
        """
        Test insert an invalid user with missing email input and password is different. Expect an error message.
        """
        errmsg = userhelper.insert_new_user("joe", "", "passwd", "passsd", "-1")
        user = User.query.filter_by(email="joe@utsc.com").first()
        # to show that insert failed
        self.assertIsNone(user)
        self.assertEqual(errmsg, (["Passwords do not match.", "An email is required."], None))

    def test_insert_user_used_email_wrong_passwd(self):
        """
        Test insert an invalid user with same email input and password is different. Expect an error message.
        """
        userhelper.insert_new_user("joe", "joe@utsc.com", "passwd", "passwd", "-1")
        user = User.query.filter_by(email="joe@utsc.com").first()
        self.assertIsNotNone(user)
        # to show the insert succeed
        errmsg = userhelper.insert_new_user("joseph", "joe@utsc.com", "passwd", "paswd", "-1")
        self.assertEqual(errmsg, (["Email has already been used.", "Passwords do not match."], None))

    def test_insert_user_blank(self):
        """
        Test insert an invalid user with all info are blank. Expect an error message.
        """
        errmsg = userhelper.insert_new_user("", "", "", "", "0")
        self.assertEqual(errmsg, (['An email is required.', 'A password is required.'], None))


if __name__ == "__main__":
    unittest.main()
