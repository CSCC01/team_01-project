import qrcode
from PIL import Image
import os

def to_qr(url, rcid):
    img = qrcode.make(url)
    path = os.getcwd()+'static/Resources/QR/'+str(rcid)+'.png'
    # how to resolve this
    img.save(path)
    return path






