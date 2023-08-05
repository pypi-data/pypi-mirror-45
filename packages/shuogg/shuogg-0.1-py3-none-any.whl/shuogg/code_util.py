import hashlib
import base64


def md5_bytes(s):
    """
    :param s:
    :return: bytes
    """
    h = hashlib.md5()
    h.update(s.encode())
    return h.digest()


def md5_string(s):
    """
    :param s:
    :return: str
    """
    h = hashlib.md5()
    h.update(s.encode())
    return h.hexdigest()


def sha1_bytes(s):
    """
    :param s:
    :return: bytes
    """
    h = hashlib.sha1()
    h.update(s.encode())
    return h.digest()  # bytes


def sha1_string(s):
    """
    :param s:
    :return: str
    """
    h = hashlib.sha1()
    h.update(s.encode())
    return h.hexdigest()  # str


def base64_encode(s):
    """
    :param s:
    return: str
    """
    bs = base64.urlsafe_b64encode(s.encode())  # bytes
    return bs.decode()


def base_decode(s):
    """
    :param s:
    :return: str
    """
    db = base64.urlsafe_b64decode(s)
    return db.decode()  # str
