import qrcode
from PIL import Image
import os
import config
from pathlib import Path

# the method of generating qr code comes from
# https://note.nkmk.me/en/python-pillow-qrcode/
def to_qr(url, uid, cid):
    img = qrcode.make(url)
    if config.STATUS == 'TEST':
        path = str(get_root()) + '/static/Resources/QR/'+str(uid)+'_'+str(cid)+'.png'
        path = path.replace("/", os.path.sep)
    else:
        path ='static/Resources/QR/'+str(uid)+'_'+str(cid)+'.png'
    # how to resolve this
    img.save(path)
    return path

def update_achievement_qr(url, aid, uid):
    """

    :param url: the url(local:127.0.0.1, remote: pickeasy-)
    :param aid: achievement id, example:5
    :param uid: user id, example:3
    :return: the img path, example: /static/Resources/QR/update_achievement/3_5.png
    """

    img = qrcode.make(url)
    if config.STATUS == 'TEST':
        path = str(get_root()) + '/static/Resources/QR/update_achievement/'+str(uid)+'_'+str(aid)+'.png'
        path = path.replace("/", os.path.sep)
    else:
        path = 'static/Resources/QR/update_achievement/'+str(uid)+'_'+str(aid)+'.png'
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



