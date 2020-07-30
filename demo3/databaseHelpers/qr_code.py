import qrcode
from PIL import Image
import os
import config
from pathlib import Path

def to_qr(url, rcid):
    img = qrcode.make(url)
    if config.STATUS == 'TEST':
        path = str(get_root()) + '/static/Resources/QR/'+str(rcid)+'.png'
        path = path.replace("/", os.path.sep)
    else:
        path ='static/Resources/QR/'+str(rcid)+'.png'
    # how to resolve this
    img.save(path)
    return path

def get_root():
    """
    Helper function for to_qr
    No need to do further test
    """
    cwd = os.getcwd()
    path = Path(cwd)
    while (str(path) != str(path.parent)):
        if str(path).endswith("demo3"):
            return path
        cwd = path.parent
        path = Path(cwd)
    return path



