import unittest
from models import Achievements
from models import db
import time
from app import app
from databaseHelpers.achievement import *


class InsertAchievementTest(unittest.TestCase):
    """
    Test function on insert achievement
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

    def test_insert_normal_zero_type(self):
        """
        test insert a normal achievement of type 0
        """
        errmsg = insert_achievement(rid=8, name='Starbucks', experience=10, points=5, type='0', item='test', amount=20)
        a = Achievements.query.filter_by(rid=8).first()
        self.assertEqual(a.name, 'Starbucks')
        self.assertEqual(a.experience, 10)
        self.assertEqual(a.points, 5)
        self.assertEqual(a.type, 0)
        self.assertEqual(a.value, 'test;20')
        self.assertEqual(errmsg, [])


    def test_insert_normal_one_type(self):
        """
        test insert a normal achievement of type 1
        """
        errmsg = insert_achievement(rid=9, name='Starbucks', experience=10, points=5, type='1', item='test', amount=20)
        a = Achievements.query.filter_by(rid=9).first()
        self.assertEqual(a.name, 'Starbucks')
        self.assertEqual(a.experience, 10)
        self.assertEqual(a.points, 5)
        self.assertEqual(a.type, 1)
        self.assertEqual(a.value, ';20')
        self.assertEqual(errmsg, [])

    def test_insert_only_exp(self):
        """
        test insert an achievement with only experience
        """
        errmsg = insert_achievement(rid=10, name='Starbucks', experience=10, points='', type='1', item='', amount=20)
        a = Achievements.query.filter_by(rid=10).first()
        self.assertEqual(a.name, 'Starbucks')
        self.assertEqual(a.experience, 10)
        self.assertEqual(a.type, 1)
        self.assertEqual(a.value, ';20')
        self.assertEqual(errmsg, [])

    def test_insert_only_points(self):
        """
        test insert an achievement with only experience
        """
        errmsg = insert_achievement(rid=11, name='Starbucks', experience='', points=20, type='0', item='test',
                                    amount=20)
        a = Achievements.query.filter_by(rid=11).first()
        self.assertEqual(a.name, 'Starbucks')
        self.assertEqual(a.points, 20)
        self.assertEqual(a.type, 0)
        self.assertEqual(a.value, 'test;20')
        self.assertEqual(errmsg, [])

    def test_insert_miss_name(self):
        """
        test insert an achievement with name missing
        """
        errmsg = insert_achievement(rid=11, name='', experience='', points=20, type='0', item='test', amount=20)
        a = Achievements.query.filter_by(rid=11).first()
        self.assertIsNone(a)
        self.assertEqual(errmsg, ["Invalid achievement name, please provide an achievement name."])

    def test_insert_miss_exp_points(self):
        """
        test insert an achievement with experience and points missing
        """
        errmsg = insert_achievement(rid=11, name='Starbucks', experience='', points='', type='0', item='test', amount=20)
        a = Achievements.query.filter_by(rid=11).first()
        self.assertIsNone(a)
        self.assertEqual(errmsg, ["Missing experience and points, please at least provide experience or points."])

    def test_insert_invalid_experience(self):
        """
        test insert an achievement with invalid experience
        """
        errmsg = insert_achievement(rid=11, name='Starbucks', experience=-10, points=5, type='0', item='test',
                                    amount=20)
        a = Achievements.query.filter_by(rid=11).first()
        self.assertIsNone(a)
        self.assertEqual(errmsg, ["Invalid experience, please provide non-negative value."])

    def test_insert_invalid_points(self):
        """
        test insert an achievement with invalid points
        """
        errmsg = insert_achievement(rid=11, name='Starbucks', experience=10, points=-5, type='0', item='test',
                                    amount=20)
        a = Achievements.query.filter_by(rid=11).first()
        self.assertIsNone(a)
        self.assertEqual(errmsg, ["Invalid points, please provide non-negative value."])

<<<<<<< HEAD
    # Test abnormal achievement creation with exp and pts both are negative
    def test_insert_abnormal_negative_both_achievement(self):
        errmsg = insert_achievement(1, "name", "description", -10, -10, None, 10, False)
        self.assertEqual(errmsg,
                        ["Invalid experience, please provide non-negative value.", "Invalid points, please provide non-negative value."])

    # Test abnormal achievement creation with feetype and require fee is empty
    def test_insert_abnormal_feetype_fee_empty_achievement(self):
        errmsg = insert_achievement(1, "name", "description", 10, 10, None, None, False)
        self.assertEqual(errmsg, ["Missing Fee."])

    # Test abnormal achievement creation with itemtype and require item is empty
    def test_insert_abnormal_itemtype_item_empty_achievement(self):
        errmsg = insert_achievement(1, "name", "description", 10, 10, None, None, True)
        self.assertEqual(errmsg, ["Missing Item."])

    # Test abnormal achievement creation with feetype and require fee is negative
    def test_insert_abnormal_feetype_fee_negative_achievement(self):
        errmsg = insert_achievement(1, "name", "description", 10, 10, None, -10, False)
        self.assertEqual(errmsg, ["Invalid requirement, please provide non-negative value."])

    # Test abnormal achievement creation with itemtype and require item is negative
    def test_insert_abnormal_feetype_item_negative_achievement(self):
        errmsg = insert_achievement(1, "name", "description", 10, 10, -10, None, True)
        self.assertEqual(errmsg, ["Invalid requirement, please provide non-negative value."])
=======
    def test_insert_miss_item(self):
        """
        test insert an achievement with item missing
        """
        errmsg = insert_achievement(rid=11, name='Starbucks', experience=10, points=5, type='0', item='',
                                    amount=20)
        a = Achievements.query.filter_by(rid=11).first()
        self.assertIsNone(a)
        self.assertEqual(errmsg, ["Missing an item, please provide an item for the achievement."])

    def test_insert_miss_amount(self):
        """
        test insert an achievement with amount missing
        """
        errmsg = insert_achievement(rid=11, name='Starbucks', experience=10, points=5, type='0', item='test', amount='')
        a = Achievements.query.filter_by(rid=11).first()
        self.assertIsNone(a)
        self.assertEqual(errmsg, ["Missing an amount, please provide an amount for the achievement."])

    def test_insert_item_with_semi(self):
        """
        test insert achievement for sanitizing input in type 0
        """
        errmsg = insert_achievement(rid=8, name='Starbucks', experience=10, points=5, type='0', item='Ham;Cheese', amount=20)
        a = Achievements.query.filter_by(rid=8).first()
        self.assertEqual(a.name, 'Starbucks')
        self.assertEqual(a.experience, 10)
        self.assertEqual(a.points, 5)
        self.assertEqual(a.type, 0)
        self.assertEqual(a.value, 'HamCheese;20')
        self.assertEqual(errmsg, [])

    def test_insert_same_achievement(self):
        """
        test for inserting achievement with the exact same detail
        make sure insert as separate achievement
        """
        e1 = insert_achievement(rid=7, name='Starbucks', experience=10, points=5, type='0', item='Ham;Cheese', amount=20)
        e2 = insert_achievement(rid=7, name='Starbucks', experience=10, points=5, type='0', item='Ham;Cheese', amount=20)
        a1 = Achievements.query.filter_by(aid=1).first()
        a2 = Achievements.query.filter_by(aid=2).first()
        self.assertIsNotNone(a1)
        self.assertIsNotNone(a2)
        self.assertEqual(e1, [])
        self.assertEqual(e2, [])


>>>>>>> origin/Development

if __name__ == "__main__":
    unittest.main()
