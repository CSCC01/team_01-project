import unittest
from app import app


class MainPageTest(unittest.TestCase):
    """
    Test page status. which should be 200.
    """

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_main_page_login_1(self):
        """
        Test for login. Expect status code 200.
        """
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_login_2(self):
        """
        Test for login. Expect status code 200.
        """
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_login_3(self):
        """
        Test for login. Expect status code 200.
        """
        response = self.app.get('/login.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_home_1(self):
        """
        Test for home page. Expect status code 200.
        """
        response = self.app.get('/home', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_home_2(self):
        """
        Test for home page. Expect status code 200.
        """
        response = self.app.get('/home.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_registration_1(self):
        """
        Test for registration page. Expect status code 200.
        """
        response = self.app.get('/registration', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_registration_2(self):
        """
        Test for registration page. Expect status code 200.
        """
        response = self.app.get('/registration.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_registration0_1(self):
        """
        Test for registration page. Expect status code 200.
        """
        response = self.app.get('/registration0', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_registration0_2(self):
        """
        Test for registration page. Expect status code 200.
        """
        response = self.app.get('/registration0.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_registration1_1(self):
        """
        Test for registration page. Expect status code 200.
        """
        response = self.app.get('/registration1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_registration1_2(self):
        """
        Test for registration page. Expect status code 200.
        """
        response = self.app.get('/registration1.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_registration2_1(self):
        """
        Test for registration page. Expect status code 200.
        """
        response = self.app.get('/registration2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_registration2_2(self):
        """
        Test for registration page. Expect status code 200.
        """
        response = self.app.get('/registration2.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_coupon_1(self):
        """
        Test for coupon page. Expect status code 200.
        """
        response = self.app.get('/coupon', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_coupon_2(self):
        """
        Test for coupon page. Expect status code 200.
        """
        response = self.app.get('/coupon.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_coupon_create_1(self):
        """
        Test for coupon creation page. Expect status code 200.
        """
        response = self.app.get('/createCoupon', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_coupon_create_2(self):
        """
        Test for coupon creation page. Expect status code 200.
        """
        response = self.app.get('/createCoupon.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_employee_1(self):
        """
        Test for employee page. Expect status code 200.
        """
        response = self.app.get('/employee', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_employee_2(self):
        """
        Test for employee page. Expect status code 200.
        """
        response = self.app.get('/employee.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_search_1(self):
        """
        Test for search page. Expect status code 200.
        """
        response = self.app.get('/search', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_search_2(self):
        """
        Test for search page. Expect status code 200.
        """
        response = self.app.get('/search.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_profile_1(self):
        """
        Test for profile page. Expect status code 200.
        """
        response = self.app.get('/profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_profile_2(self):
        """
        Test for profile page. Expect status code 200.
        """
        response = self.app.get('/profile.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_logout_1(self):
        """
        Test for logout page. Expect status code 200.
        """
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_logout_2(self):
        """
        Test for logout page. Expect status code 200.
        """
        response = self.app.get('/logout.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)




if __name__ == "__main__":
    unittest.main()