import requests


def request_json(method, url, data=None, headers=None, cookies=None):
    """
     eg:request("GET", "127.0.0.1:8000")
    :param method: 'GET' 'POST' 'PUT' 'DELETE'
    :param url: str
    :param data: dict
    :param headers: dict
    :param cookies: dict
    :return: (int, dict)
    """
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    r = requests.request(method, url, data=data, headers=headers, cookies=cookies)
    print(url)
    print(r.status_code, r.json())
    if r.status_code != 200:
        return r.status_code, r.text
    return r.status_code, r.json()


def request(method, url, data=None, headers=None, cookies=None):
    """
     eg:request("GET", "127.0.0.1:8000")
    :param method: 'GET' 'POST' 'PUT' 'DELETE'
    :param url: str
    :param data: dict
    :param headers: dict
    :param cookies: dict
    :return: (int, str)
    """
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    r = requests.request(method, url, data=data, headers=headers, cookies=cookies)
    print(url)
    print(r.status_code, r.text)
    return r.status_code, r.text


if __name__ == '__main__':
    request("GET", "127.0.0.1:8000/p/wechat/mp/jsapi/signature")
