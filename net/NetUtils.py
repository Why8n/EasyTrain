import requests
import time

from define.UserAgent import FIREFOX_USER_AGENT


def sendLogic(func):
    def wrapper(*args, **kw):
        for count in range(10):
            response = func(*args, **kw)
            if response:
                return response
            else:
                time.sleep(0.1)
        return None

    return wrapper


class EasyHttp(object):
    __session = requests.Session()

    @staticmethod
    def updateHeaders(headers):
        EasyHttp.__session.headers.update(headers)

    @staticmethod
    def resetHeaders():
        EasyHttp.__session.headers.clear()
        EasyHttp.__session.headers.update({
            'Host': r'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
            'User-Agent': FIREFOX_USER_AGENT,
        })

    @staticmethod
    def setCookies(**kwargs):
        for k, v in kwargs.items():
            EasyHttp.__session.cookies.set(k, v)

    @staticmethod
    def removeCookies(key=None):
        EasyHttp.__session.cookies.set(key, None) if key else EasyHttp.__session.cookies.clear()

    @staticmethod
    @sendLogic
    def send(urlInfo, params=None, data=None, **kwargs):
        EasyHttp.resetHeaders()
        if 'headers' in urlInfo and urlInfo['headers']:
            EasyHttp.updateHeaders(urlInfo['headers'])
        try:
            response = EasyHttp.__session.request(method=urlInfo['method'],
                                                  url=urlInfo['url'],
                                                  params=params,
                                                  data=data,
                                                  timeout=10,
                                                  allow_redirects=False,
                                                  **kwargs)
            if response.status_code == requests.codes.ok:
                if 'response' in urlInfo:
                    if urlInfo['response'] == 'binary':
                        return response.content
                    if urlInfo['response'] == 'html':
                        response.encoding = response.apparent_encoding
                        return response.text
                return response.json()
        except:
            pass
        return None


if __name__ == '__main__':
    pass
