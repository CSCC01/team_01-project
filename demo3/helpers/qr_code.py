import qrcode
from PIL import Image
import os
import config
from pathlib import Path

cwd = os.getcwd()
path = Path(cwd)
cwd_p = path.parent
path_p = Path(cwd_p)
cwd_pp = path_p.parent

def to_qr(url, rcid):
    img = qrcode.make(url)
    if config.STATUS == 'TEST':
        path = str(cwd_pp) + '/static/Resources/QR/'+str(rcid)+'.png'
    else:
        path ='static/Resources/QR/'+str(rcid)+'.png'
    # how to resolve this
    img.save(path)
    return path




