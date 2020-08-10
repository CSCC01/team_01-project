import unittest
from models import User, Restaurant, Experience
from models import db
import time
from app import app
from databaseHelpers import experience as experiencehelper

class InsertExperienceTest(unittest.TestCase):
    '''
    Tests insert_experience() in databaseHelpers/experience.py.
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

    def test_insert_standard_experience_entry(self):
        '''
        Tests inserting a normal entry with no issues into the experience table. Expect output to match correct data.
        '''
        errmsg = experiencehelper.insert_experience(1, 12)
        self.assertEqual(errmsg, None)

        experience = Experience.query.filter_by(uid=1, rid=12).first()
        self.assertNotEqual(experience, None)
        self.assertEqual(experience.uid, 1)
        self.assertEqual(experience.rid, 12)
        self.assertEqual(experience.experience, 0)

    def test_insert_duplicate_uid_experience_entry(self):
        '''
        Tests inserting an entry into the experience table while an entry with
        the same uid and a different rid already exists in the table. Expect output to match correct data.
        '''
        experience = Experience(uid=1, rid=12, experience=10)
        db.session.add(experience)
        errmsg = experiencehelper.insert_experience(1, 13)
        self.assertEqual(errmsg, None)

        experience = Experience.query.filter_by(uid=1)
        self.assertEqual(experience.count(), 2)

        experience = Experience.query.filter_by(uid=1, rid=12).first()
        self.assertNotEqual(experience, None)
        self.assertEqual(experience.uid, 1)
        self.assertEqual(experience.rid, 12)
        self.assertEqual(experience.experience, 10)

        experience = Experience.query.filter_by(uid=1, rid=13).first()
        self.assertNotEqual(experience, None)
        self.assertEqual(experience.uid, 1)
        self.assertEqual(experience.rid, 13)
        self.assertEqual(experience.experience, 0)

    def test_insert_duplicate_rid_experience_entry(self):
        '''
        Tests inserting an entry into the experience table while an entry with
        the same rid and a different uid already exists in the table. Expect output to match correct data.
        '''
        experience = Experience(uid=1, rid=12, experience=10)
        db.session.add(experience)
        errmsg = experiencehelper.insert_experience(2, 12)
        self.assertEqual(errmsg, None)

        experience = Experience.query.filter_by(rid=12)
        self.assertEqual(experience.count(), 2)

        experience = Experience.query.filter_by(uid=1, rid=12).first()
        self.assertNotEqual(experience, None)
        self.assertEqual(experience.uid, 1)
        self.assertEqual(experience.rid, 12)
        self.assertEqual(experience.experience, 10)

        experience = Experience.query.filter_by(uid=2, rid=12).first()
        self.assertNotEqual(experience, None)
        self.assertEqual(experience.uid, 2)
        self.assertEqual(experience.rid, 12)
        self.assertEqual(experience.experience, 0)

    def test_insert_duplicate_uid_and_rid_experience_entry(self):
        '''
        Tests inserting an entry into the experience table while an entry with
        the same uid and same rid already exists in the table. Expect an error message and data in database remains the same.
        '''
        experience = Experience(uid=1, rid=12, experience=10)
        db.session.add(experience)
        errmsg = experiencehelper.insert_experience(1, 12)
        self.assertEqual(errmsg, ["Experience entry already exists for given user at this restaurant."])

        experience = Experience.query.filter_by(uid=1, rid=12)
        self.assertEqual(experience.count(), 1)
        self.assertEqual(experience.first().uid, 1)
        self.assertEqual(experience.first().rid, 12)
        self.assertEqual(experience.first().experience, 10)




if __name__ == "__main__":
    unittest.main()
