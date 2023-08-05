import base64
from pyDes import *


def encrypt(key, content):
    k = des(key.encode(), padmode=PAD_PKCS5)
    des_bytes = k.encrypt(content)
    return base64.b64encode(des_bytes).decode('ascii')
