import unittest
from models import Customer_Achievement_Progress, Points, User, Achievements
from models import db
from app import app
from databaseHelpers import achievementProgress as achievementhelper


class GetProgressCompletionStatusTest(unittest.TestCase):
    """
    Tests get_progress_completion_status() in achievementProgress.py
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

    def test_progress_not_found(self):
        '''
        Check status of a nonexistent achievement progress entry
        '''
        self.assertEqual(achievementhelper.get_progress_completion_status('Not Found'), 0)

    def test_progress_incomplete(self):
        '''
        Check status of an incomplete achievement progress entry
        '''
        progress = Customer_Achievement_Progress(aid=1, uid=3, progress=3, total=4)
        self.assertEqual(achievementhelper.get_progress_completion_status(progress), 1)

    def test_progress_complete(self):
        '''
        Check status of a complete achievement progress entry
        '''
        progress = Customer_Achievement_Progress(aid=1, uid=3, progress=4, total=4)
        self.assertEqual(achievementhelper.get_progress_completion_status(progress), 2)



if __name__ == "__main__":
    unittest.main()
