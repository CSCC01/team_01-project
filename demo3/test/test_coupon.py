from flask import Flask, session
from app import app
from exts import db
from models import Coupon
import config
import os
import unittest


class CouponDBTest(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.testing = True
        self.app = Flask(__name__)
        db.init_app(self.app)
        app.config["SQLALCHEMY_DATABASE_URI"] = \
            "mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8".format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
        app.config['WTF_CSRF_ENABLED'] = False
        db.create_all()
        pass
    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        pass

    # Back end starts

    # Testing normal coupon code creation back-end(database insertion).
    # Creating a normal coupon code and test after inserting it to the 
    # database by seeing if it stores correctly
    def test_coupon_creation_normal_with_date(self):
        coupon = Coupon(rid = 2, name = "50%", description = "for national day", cost = 100, expiration = '2020-11-15', begin = '2020-11-14')
        db.session.add(coupon)
        db.session.commit()
        time.sleep(10)
        coupon = Coupon.query.filter_by(rid=2)
        self.assertIsNotNone(coupon)
        self.assertGreater(coupon.cid, 0)
        self.assertEqual(coupon.name, "50%")
        self.assertEqual(coupon.description, "for national day")
        self.assertEqual(coupon.cost, 100)
        self.assertEqual(coupon.expiration, '2020-11-15')
        self.assertEqual(coupon.begin, '2020-11-14')
    
    # As we can have infinite time for coupon suggested by client, we will have the case that coupon's expiration and begin are 
    # empty.
    def test_coupon_creation_normal_without_date(self):
        coupon = Coupon(rid = 2, name = "50%", description = "for national day", cost = 100, expiration = '', begin = '')
        db.session.add(coupon)
        db.session.commit()
        time.sleep(10)
        coupon = Coupon.query.filter_by(rid=2)
        self.assertIsNotNone(coupon)
        self.assertGreater(coupon.cid, 0)
        self.assertEqual(coupon.name, "50%")
        self.assertEqual(coupon.description, "for national day")
        self.assertEqual(coupon.cost, 100)
        self.assertEqual(coupon.expiration, '')
        self.assertEqual(coupon.begin, '')
    # Back end ends

    # All starts
    
    #################
    ### base case ###
    #################
    
    # Testing normal coupon creation
    def test_coupon_creation_normal_all(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, "for national day", '2020-11-15', '2020-11-14', False)
        self.assertIsNotNone(response.data)
        self.assertNotIn(b'Invalid amount for points.', response.data)
        self.assertNotIn(b'Invalid coupon name, please give your coupon a name.', response.data)
        self.assertNotIn(b'Invalid coupon description, please give your coupon a description.', response.data)
        self.assertNotIn(b'Missing start or expiration date.', response.data)
    

    ######################
    ### Testing points ###
    ######################

    # Testing normal coupon creation with point value is 0, it is valid
    def test_coupon_creation_point_zero(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 0, "for national day", '2020-11-15', '2020-11-14', False)
        self.assertIsNotNone(response.data)
        self.assertNotIn(b'Invalid amount for points.', response.data)
        self.assertNotIn(b'Invalid coupon name, please give your coupon a name.', response.data)
        self.assertNotIn(b'Invalid coupon description, please give your coupon a description.', response.data)
        self.assertNotIn(b'Missing start or expiration date.', response.data)
    
    # Testing abnormal coupon creation with points field is empty
    def test_coupon_creation_point_empty(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", "", "for national day", '2020-11-15', '2020-11-14', False)
        self.assertIn(b'Invalid amount for points.', response.data)

    # Testing abnormal coupon creation with point's value is negative
    def test_coupon_creation_point_negative(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", -12, "for national day", '2020-11-15', '2020-11-14', False)
        self.assertIn(b'Invalid amount for points.', response.data)
    

    ####################
    ### Testing name ###
    ####################

    # Testing abnormal coupon creation with name is empty
    def test_coupon_creation_name_empty(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "", 100, "for national day", '2020-11-15', '2020-11-14', False)
        self.assertIn(b'Invalid coupon name, please give your coupon a name.', response.data)
    
    # Testing abnormal coupon creation with name is NULL
    def test_coupon_creation_name_NULL(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            NULL, 100, "for national day", '2020-11-15', '2020-11-14', False)
        self.assertIn(b'Invalid coupon name, please give your coupon a name.', response.data)


    ###########################
    ### Testing description ###
    ###########################
    
    # Testing abnormal coupon creation with description is empty
    def test_coupon_creation_description_empty(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, "", '2020-11-15', '2020-11-14', False)
        self.assertIn(b'Invalid coupon description, please give your coupon a description.', response.data)

    # Testing abnormal coupon creation with description is NULL
    def test_coupon_creation_description_NULL(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, NULL, '2020-11-15', '2020-11-14', False)
        self.assertIn(b'Invalid coupon description, please give your coupon a description.', response.data)

    # Testing abnormal coupon creation with description is out of bound
    def test_coupon_creation_description_out(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        tem_des = "a" * 63 + '\0' 
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, tem_des, '2020-11-15', '2020-11-14', False)
        self.assertIn(b'Invalid coupon description, please give your coupon a description.', response.data)


    ####################################
    ### Testing expiration and begin ###
    ####################################

    # Testing abnormal coupon creation with expiration/begin date is empty and indefinite is false
    def test_coupon_creation_expiration_empty(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, "for national day", '', '2020-11-14', False)
        self.assertIn(b'Missing start or expiration date.', response.data)

    def test_coupon_creation_begin_empty(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, "for national day", '2020-11-15', '', False)
        self.assertIn(b'Missing start or expiration date.', response.data)
    
    # Testing abnormal coupon creation with expiration&begin date are empty and indefinite is false
    def test_coupon_creation_both_empty(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, "for national day", '', '', False)
        self.assertIn(b'Missing start or expiration date.', response.data)

    # Testing abnormal coupon creation with expiration/begin date is NULL and indefinite is false
    def test_coupon_creation_expiration_NULL(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, "for national day", NULL, '2020-11-14', False)
        self.assertIn(b'Missing start or expiration date.', response.data)
    
    def test_coupon_creation_begin_NULL(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, "for national day", '2020-11-15', NULL, False)
        self.assertIn(b'Missing start or expiration date.', response.data)

    # Testing abnormal coupon creation with expiration&begin date are NULL and indefinite is false
    def test_coupon_creation_both_NULL(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, "for national day", NULL, NULL, False)
        self.assertNotIn(b'Missing start or expiration date.', response.data)

    # Testing abnormal coupon creation with expiration/begin date is empty and indefinite is true
    def test_coupon_creation_expiration_empty_infin(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, "for national day", '', '2020-11-14', True)
        self.assertIn(b'Missing start or expiration date.', response.data)

    def test_coupon_creation_begin_empty_infin(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, "for national day", '2020-11-15', '', True)
        self.assertIn(b'Missing start or expiration date.', response.data)

    # Testing normal coupon creation with expiration&begin date are empty and indefinite is true
    def test_coupon_creation_both_empty_infin(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, "for national day", '', '', True)
        self.assertIsNotNone(response.data)
        self.assertNotIn(b'Invalid amount for points.', response.data)
        self.assertNotIn(b'Invalid coupon name, please give your coupon a name.', response.data)
        self.assertNotIn(b'Invalid coupon description, please give your coupon a description.', response.data)
        self.assertNotIn(b'Missing start or expiration date.', response.data)

    # Testing abnormal coupon creation with expiration/begin date is NULL and indefinite is true
    def test_coupon_creation_expiration_NULL_infin(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, "for national day", NULL, '2020-11-14', True)
        self.assertIn(b'Missing start or expiration date.', response.data)

    def test_coupon_creation_begin_NULL_infin(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, "for national day", '2020-11-15', NULL, True)
        self.assertIn(b'Missing start or expiration date.', response.data)

    # Testing normal coupon creation with expiration&begin date are NULL and indefinite is true
    def test_coupon_creation_both_NULL_infin(self):
        response_owner = self.register_owner(self, "abc", "abc@mail.com", "pass", "abc", "abc") 
        response_own_login = self.login_owner(self, "abc@mail.com", "pass")
        response = self.create_coupon_helper(self, Restaurant.query.filter(Restaurant.uid == session['account']).first().rid,
                                            "50%", 100, "for national day", NULL, NULL, True)
        self.assertIsNotNone(response.data)
        self.assertNotIn(b'Invalid amount for points.', response.data)
        self.assertNotIn(b'Invalid coupon name, please give your coupon a name.', response.data)
        self.assertNotIn(b'Invalid coupon description, please give your coupon a description.', response.data)
        self.assertNotIn(b'Missing start or expiration date.', response.data)

    # All ends

    ##############
    ### helper ###
    ##############

    def create_coupon_helper(self, rid, name, points, description, expiration, begin, indefinite):
        return self.post('/createCoupon', data = dict (
            rid = rid, 
            name = name, 
            points = points, 
            description = description,
            expiration = expiration,
            begin = begin,
            indefinite = indefinite
        ), follow_redirects=True)
    
    def register_owner(self, name, email, password, address, rname):
        return self.post('/registration1', data = dict (
            name = name,
            email = email,
            password = password,
            password2 = password,
            address = address,
            rname = rname
        ), follow_redirects=True)
    
    def login_owner(self, email, password):
        return self.post('/login', data = dict (
            email = email,
            password = password
        ), follow_redirects=True)
