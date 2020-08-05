import unittest
from models import User, Restaurant, Experience
from models import db
import time
from app import app
from databaseHelpers import experience as experiencehelper

class SelectExperienceTest(unittest.TestCase):
    '''
    Tests get_experience() in databaseHelpers/experience.py.
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

    def test_get_existing_experience_entry(self):
        '''
        Tests selecting a normal entry with no issues from the the experience table.
        '''
        newEntry = Experience(uid=1, rid=12, experience=10)
        db.session.add(newEntry)
        db.session.commit()
        experience = experiencehelper.get_experience(1, 12)
        self.assertNotEqual(experience, None)
        self.assertEqual(experience.uid, 1)
        self.assertEqual(experience.rid, 12)
        self.assertEqual(experience.experience, 10)

    def test_get_nonexistent_experience_entry(self):
        '''
        Tests trying to select an entry that does not exist from the experience table.
        '''
        newEntry = Experience(uid=1, rid=13, experience=10)
        db.session.add(newEntry)
        db.session.commit()
        experience = experiencehelper.get_experience(2, 12)
        self.assertEqual(experience, None)

    def test_get_nonexistent_experience_entry_duplicate_uid(self):
        '''
        Tests trying to select an entry that does not exist from the experience table,
        while an entry with the same uid and different rid does exist in the table.
        '''
        newEntry = Experience(uid=1, rid=13, experience=10)
        db.session.add(newEntry)
        db.session.commit()
        experience = experiencehelper.get_experience(1, 12)
        self.assertEqual(experience, None)

    def test_get_nonexistent_experience_entry_duplicate_rid(self):
        '''
        Tests trying to select an entry that does not exist from the experience table,
        while an entry with the same rid and different uid does exist in the table.
        '''
        newEntry = Experience(uid=1, rid=13, experience=10)
        db.session.add(newEntry)
        db.session.commit()
        experience = experiencehelper.get_experience(2, 13)
        self.assertEqual(experience, None)


if __name__ == "__main__":
    unittest.main()
