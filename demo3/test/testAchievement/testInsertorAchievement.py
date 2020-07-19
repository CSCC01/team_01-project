import unittest
from models import Achievement
from models import db
import time
from app import app
from helpers.achievement import *

class InsertAchievementTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Test normal achievement creation with Fee type
    def test_insert_default_normal_Feetype_achievement(self):
        errmsg = insert_achievement(1, "name", "description", 10, 10, None, 10, False)
        achievement = Achievement.query.filter_by(rid = 1, name = "name").first()
        self.assertIsNone(achievement)
        self.assertEqual(achievement.cid, 1)
        self.assertEqual(achievement.rid, 1)
        self.assertEqual(achievement.name, "name")
        self.assertEqual(achievement.description, "description")
        self.assertEqual(achievement.experience, 10)
        self.assertEqual(achievement.points, 10)
        self.assertEqual(achievement.requireFee, 10)
        self.assertIsNone(achievement.requireItem)
        self.assertIsNone(errmsg)

    # Test normal achievement creation with only experience reward
    def test_insert_default_normal_exp_only_achievement(self):
        errmsg = insert_achievement(1, "name", "description", 10, None, None, 10, False)
        achievement = Achievement.query.filter_by(rid = 1, name = "name").first()
        self.assertIsNone(achievement)
        self.assertEqual(achievement.cid, 1)
        self.assertEqual(achievement.rid, 1)
        self.assertEqual(achievement.name, "name")
        self.assertEqual(achievement.description, "description")
        self.assertEqual(achievement.experience, 10)
        self.assertIsNone(achievement.points)
        self.assertEqual(achievement.requireFee, 10)
        self.assertIsNone(achievement.requireItem)
        self.assertIsNone(errmsg)

    # Test normal achievement creation with only points reward
    def test_insert_default_normal_pts_only_achievement(self):
        errmsg = insert_achievement(1, "name", "description", None, 10, None, 10, False)
        achievement = Achievement.query.filter_by(rid = 1, name = "name").first()
        self.assertIsNone(achievement)
        self.assertEqual(achievement.cid, 1)
        self.assertEqual(achievement.rid, 1)
        self.assertEqual(achievement.name, "name")
        self.assertEqual(achievement.description, "description")
        self.assertIsNone(achievement.experience)
        self.assertEqual(achievement.points, 10)
        self.assertEqual(achievement.requireFee, 10)
        self.assertIsNone(achievement.requireItem)
        self.assertIsNone(errmsg)

    # Test normal achievement creation with Item type
    def test_insert_default_normal_Itemtype_achievement(self):
        errmsg = insert_achievement(1, "name", "description", 10, 10, 12, None, True)
        achievement = Achievement.query.filter_by(rid = 1, name = "name").first()
        self.assertIsNone(achievement)
        self.assertEqual(achievement.cid, 1)
        self.assertEqual(achievement.rid, 1)
        self.assertEqual(achievement.name, "name")
        self.assertEqual(achievement.description, "description")
        self.assertEqual(achievement.experience, 10)
        self.assertEqual(achievement.points, 10)
        self.assertEqual(achievement.requireItem, 12)
        self.assertIsNone(achievement.requireFee)
        self.assertIsNone(errmsg)

    # Test abnormal achievement creation with name is empty
    def test_insert_abnormal_name_empty_achievement(self):
        errmsg = insert_achievement(1, "", "description", 10, 10, None, 10, False)
        self.assertEqual(errmsg, "Invalid achievement name, please provide an achieve name.")

    # Test abnormal achievement creation with description is empty
    def test_insert_abnormal_descrip_empty_achievement(self):
        errmsg = insert_achievement(1, "name", "", 10, 10, None, 10, False)
        self.assertEqual(errmsg, "Invalid description of achievement, please provide a description.")

    # Test abnormal achievement creation with Fee type
    def test_insert_abnormal_exp_pts_both_empty_achievement(self):
        errmsg = insert_achievement(1, "name", "description", "", "", None, 10, False)
        self.assertEqual(errmsg, "Missing experience and points, please at least provide experience or points.")

    # Test abnormal achievement creation with exp is negative
    def test_insert_abnormal_negative_exp_achievement(self):
        errmsg = insert_achievement(1, "name", "description", -10, 10, None, 10, False)
        self.assertEqual(errmsg, "Invalid experience, please provide non-negative value.")

    # Test abnormal achievement creation with points is negative
    def test_insert_abnormal_negative_pts_achievement(self):
        errmsg = insert_achievement(1, "name", "description", 10, -10, None, 10, False)
        self.assertEqual(errmsg, "Invalid points, please provide non-negative value.")

    # Test abnormal achievement creation with exp and pts both are negative
    def test_insert_abnormal_negative_both_achievement(self):
        errmsg = insert_achievement(1, "name", "description", -10, -10, None, 10, False)
        self.assertEqual(errmsg, "Invalid experience and points, please provide non-negative value.")

    # Test abnormal achievement creation with feetype and require fee is empty
    def test_insert_abnormal_feetype_fee_empty_achievement(self):
        errmsg = insert_achievement(1, "name", "description", 10, 10, None, None, False)
        self.assertEqual(errmsg, "Missing Fee.")
    
    # Test abnormal achievement creation with itemtype and require item is empty
    def test_insert_abnormal_itemtype_item_empty_achievement(self):
        errmsg = insert_achievement(1, "name", "description", 10, 10, None, None, True)
        self.assertEqual(errmsg, "Missing Item.")
    
    # Test abnormal achievement creation with feetype and require fee is negative
    def test_insert_abnormal_feetype_fee_negative_achievement(self):
        errmsg = insert_achievement(1, "name", "description", 10, 10, None, -10, False)
        self.assertEqual(errmsg, "Invalid requirement, please provide non-negative value.")

    # Test abnormal achievement creation with itemtype and require item is negative
    def test_insert_abnormal_feetype_item_negative_achievement(self):
        errmsg = insert_achievement(1, "name", "description", 10, 10, -10, None, True)
        self.assertEqual(errmsg, "Invalid requirement, please provide non-negative value.")

if __name__ == "__main__":
    unittest.main()