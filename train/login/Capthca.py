import random

import os

from define.Const import TYPE_LOGIN_NORMAL_WAY, TYPE_LOGIN_OTHER_WAY
from define.UserAgent import USER_AGENT, FIREFOX_USER_AGENT
from net import NetUtils
from train.login import damatuWeb
from utils import FileUtils
from utils.Log import Log


class Captcha(object):
    __REPONSE_NORMAL_CDOE_SUCCESSFUL = '4'
    __REPONSE_OHTER_CDOE_SUCCESSFUL = '1'
    __CAPTCHA_PATH = 'captcha.jpg'

    def __init__(self, session):
        self.__session = session

    def getCaptcha(self, type=TYPE_LOGIN_NORMAL_WAY):
        url = r'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&{}' \
            .format(random.random()) if type == TYPE_LOGIN_OTHER_WAY \
            else r'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login' \
                 r'&rand=sjrand&{}'.format(random.random())
        print('catpchatImgURL: %s' % url)
        headers = {
            'Referer': r'https://kyfw.12306.cn/otn/login/init',
            'User-Agent': FIREFOX_USER_AGENT,
        }
        response = NetUtils.get(self.__session, url, headers=headers, verify=False)
        if response:
            return FileUtils.saveBinary(Captcha.__CAPTCHA_PATH, response.content)
        return None

    def check(self, results, type=TYPE_LOGIN_NORMAL_WAY):
        if type == TYPE_LOGIN_OTHER_WAY:
            return self._checkRandCodeAnsyn(results)
        return self._captchaCheck(results)

    def _checkRandCodeAnsyn(self, results):
        url = r'https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn'
        formData = {
            'randCode': results,
            'rand': 'sjrand',
        }
        headers = {
            'User-Agent': FIREFOX_USER_AGENT,
            'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': r'https://kyfw.12306.cn/otn/login/init',
        }
        response = NetUtils.post(self.__session, url, data=formData, headers=headers)
        print('checkCodeAsync: %s' % response.text)
        response = response.json()

        def verify(response):
            return response['status'] and Captcha.__REPONSE_OHTER_CDOE_SUCCESSFUL == response['data']['result']

        return verify(response)

    def _captchaCheck(self, results):
        url = r'https://kyfw.12306.cn/passport/captcha/captcha-check'
        data = {
            'answer': results,
            'login_site': 'E',
            'rand': 'sjrand',
        }
        headers = {
            'User-Agent': FIREFOX_USER_AGENT,
            'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': r'https://kyfw.12306.cn/otn/login/init',
        }
        response = NetUtils.post(self.__session, url, data=data, headers=headers)
        print('captchaCheck: %s' % response.text)
        response = response.json()

        def verify(response):
            return Captcha.__REPONSE_NORMAL_CDOE_SUCCESSFUL == response['result_code'] if 'result_code' in response else False

        return verify(response)

    def verifyCaptchaByClound(self):
        self.getCaptcha()
        results = damatuWeb.verify(Captcha.__CAPTCHA_PATH)
        results = self.__transCaptchaResults(results)
        Log.v('captchaResult: %s' % results)
        return results,self.check(results)

    def verifyCaptchaByHand(self, type=TYPE_LOGIN_NORMAL_WAY):
        print('captcha_path: %s%s' % (os.getcwd(), self.getCaptcha().name))
        results = input('输入验证码: ')
        Log.v('captchaResult: %s' % results)
        return results,self.check(results,type)

    def __transCaptchaResults(self, results):
        if type(results) != str:
            return ''
        offsetY = 30
        results = results.replace(r'|', r',').split(r',')
        for index in range(0, len(results)):
            if index % 2 != 0:
                results[index] = str(int(results[index]) - offsetY)
        return ','.join(results)


if __name__ == '__main__':
    pass

