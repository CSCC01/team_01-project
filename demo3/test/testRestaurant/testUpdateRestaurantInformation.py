import unittest
from models import Restaurant
from models import db
import time
from app import app
from databaseHelpers import restaurant as rhelper


class UpdateRestaurantInformationTest(unittest.TestCase):
    """
    Tests update_restaurant_information() in databaseHelpers/restaurant.py
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

    def test_restaurant_name_empty(self):
        ''' Tries to update restaurant information using an empty
        restaurant name. '''
        restaurant = Restaurant(name = "test name", address = "test address", uid = 10)
        db.session.add(restaurant)
        db.session.commit()

        errmsg = rhelper.update_restaurant_information(restaurant, "", "new address")
        self.assertEqual(errmsg, ["The restaurant's name cannot be empty."])

        updatedRestaurant = Restaurant.query.filter(Restaurant.rid == 1).first()
        self.assertEqual(updatedRestaurant.name, "test name")
        self.assertEqual(updatedRestaurant.address, "test address")
        self.assertEqual(updatedRestaurant.uid, 10)
    
    def test_restaurant_address_empty(self):
        ''' Tries to update restaurant information using an empty
        restaurant address. '''
        restaurant = Restaurant(name = "test name", address = "test address", uid = 10)
        db.session.add(restaurant)
        db.session.commit()

        errmsg = rhelper.update_restaurant_information(restaurant, "new name", "")
        self.assertEqual(errmsg, ["The restaurant's address cannot be empty."])

        updatedRestaurant = Restaurant.query.filter(Restaurant.rid == 1).first()
        self.assertEqual(updatedRestaurant.name, "test name")
        self.assertEqual(updatedRestaurant.address, "test address")
        self.assertEqual(updatedRestaurant.uid, 10)
        

    def test_restaurant_address_and_name_empty(self):
        ''' Tries to update restaurant information using an empty
        restaurant name and address. '''
        restaurant = Restaurant(name = "test name", address = "test address", uid = 10)
        db.session.add(restaurant)
        db.session.commit()

        errmsg = rhelper.update_restaurant_information(restaurant, "", "")
        self.assertEqual(errmsg, ["The restaurant's name cannot be empty.",
            "The restaurant's address cannot be empty."])

        updatedRestaurant = Restaurant.query.filter(Restaurant.rid == 1).first()
        self.assertEqual(updatedRestaurant.name, "test name")
        self.assertEqual(updatedRestaurant.address, "test address")
        self.assertEqual(updatedRestaurant.uid, 10)

    def test_restaurant_address_and_name_nonempty(self):
        ''' Tries to update restaurant information using a non-empty
        restaurant name and address.'''
        restaurant = Restaurant(name = "test name", address = "test address", uid = 10)
        db.session.add(restaurant)
        db.session.commit()

        errmsg = rhelper.update_restaurant_information(restaurant, "new name", "new address")
        self.assertEqual(errmsg, [])

        updatedRestaurant = Restaurant.query.filter(Restaurant.rid == 1).first()
        self.assertEqual(updatedRestaurant.name, "new name")
        self.assertEqual(updatedRestaurant.address, "new address")
        self.assertEqual(updatedRestaurant.uid, 10)
        


if __name__ == "__main__":
    unittest.main()
