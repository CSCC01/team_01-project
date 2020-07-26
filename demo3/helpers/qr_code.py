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


to_qr("http://localhost:5000/test/100")
to_qr("https://pickeasy-beta.herokuapp.com/test/2")
to_qr("http://127.0.0.1:5000/test/" + str(4))




