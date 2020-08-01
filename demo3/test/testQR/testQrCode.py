import unittest
from databaseHelpers.qr_code import *
import os

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
        target = str(self.get_root()) + '/static/Resources/QR/'+str(10)+'.png'
        target = target.replace("/", os.path.sep)
        self.assertEqual(path, target)

    def get_root(self):
        cwd = os.getcwd()
        path = Path(cwd)
        while (str(path) != str(path.parent)):
            if str(path).endswith("demo3"):
                return path
            cwd = path.parent
            path = Path(cwd)
        return path

if __name__ == "__main__":
    unittest.main()
