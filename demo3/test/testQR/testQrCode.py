import unittest
from helpers.qr_code import *
import os
from app import cwd

cwd = os.getcwd()
path = Path(cwd)
cwd_p = path.parent
path_p = Path(cwd_p)
cwd_pp = path_p.parent


class testQrCode(unittest.TestCase):
    """
    Test the to_qr function in qr_code helper
    Can only check path
    """
    def test_path_normal_url_to_img(self):
        """
        Test with url to check if it can be saved in correct destination
        """
        path = to_qr("iamurl",10)
        target = str(cwd_pp) + '/static/Resources/QR/'+str(10)+'.png'
        self.assertEqual(path, target)

if __name__ == "__main__":
    unittest.main()