import unittest
from models import User, Restaurant, Experience
from models import db
import time
from app import app
from databaseHelpers import experience as experiencehelper

class UpdateExperienceTest(unittest.TestCase):
    '''
    Tests update_experience() in databaseHelpers/experience.py.
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

    def test_update_nonexistent_experience_entry(self):
        '''
        Tests trying to update an entry that does not exist in the experience table. Expect an error message.
        '''
        experience = Experience(uid=1, rid=13, experience=10)
        db.session.add(experience)
        db.session.commit()
        errmsg = experiencehelper.update_experience(1, 12, 10)
        self.assertEqual(errmsg, ["Experience entry does not exist for the given user ID and restaurant ID."])

    def test_update_experience_entry_positive_increment(self):
        '''
        Tests trying to update an entry in the experience table by incrementing
        experience by a positive amount. Expect output to match correct data.
        '''
        experience = Experience(uid=1, rid=12, experience=10)
        db.session.add(experience)
        db.session.commit()
        errmsg = experiencehelper.update_experience(1, 12, 10)
        self.assertEqual(errmsg, None)

        experience = Experience.query.filter_by(uid=1, rid=12).first()
        self.assertNotEqual(experience, None)
        self.assertEqual(experience.uid, 1)
        self.assertEqual(experience.rid, 12)
        self.assertEqual(experience.experience, 20)

    def test_update_experience_entry_zero_increment(self):
        '''
        Tests trying to update an entry in the experience table by incrementing
        experience by zero. Expect output to match correct data.
        '''
        experience = Experience(uid=1, rid=12, experience=10)
        db.session.add(experience)
        db.session.commit()
        errmsg = experiencehelper.update_experience(1, 12, 0)
        self.assertEqual(errmsg, None)

        experience = Experience.query.filter_by(uid=1, rid=12).first()
        self.assertNotEqual(experience, None)
        self.assertEqual(experience.uid, 1)
        self.assertEqual(experience.rid, 12)
        self.assertEqual(experience.experience, 10)

    def test_update_experience_entry_negative_increment(self):
        '''
        Tests trying to update an entry in the experience table by incrementing
        experience by a negative amount. Expect an error message and data in database remains the same.
        '''
        experience = Experience(uid=1, rid=12, experience=10)
        db.session.add(experience)
        db.session.commit()
        errmsg = experiencehelper.update_experience(1, 12, -5)
        self.assertEqual(errmsg, ["Experience cannot be incremented by a negative number."])

        experience = Experience.query.filter_by(uid=1, rid=12).first()
        self.assertNotEqual(experience, None)
        self.assertEqual(experience.uid, 1)
        self.assertEqual(experience.rid, 12)
        self.assertEqual(experience.experience, 10)


if __name__ == "__main__":
    unittest.main()
