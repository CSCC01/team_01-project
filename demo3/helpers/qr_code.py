import qrcode
from PIL import Image
import os


import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


def to_qr(url):
    img = qrcode.make(url)
    path = 'static/Resources/qr_code.png'
    # how to resolve this
    img.save(path)
    return path






