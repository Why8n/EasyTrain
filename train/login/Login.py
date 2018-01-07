from pprint import pprint

from define.Const import TYPE_LOGIN_NORMAL_WAY, TYPE_LOGIN_OTHER_WAY
from define.UserAgent import FIREFOX_USER_AGENT
from net import NetUtils
from train.login.Capthca import Captcha
from utils import Utils
from utils.Log import Log


class Login(object):
    __LOGIN_SUCCESS_RESULT_CODE = 0

    def __init__(self, session):
        self.__session = session

    def _passportRedirect(self):
        url = r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'
        params = {
            'redirect': '/otn/login/userLogin',
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'User-Agent': FIREFOX_USER_AGENT,
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        NetUtils.get(self.__session, url, params=params, headers=headers)

    def _userLogin(self):
        url = r'https://kyfw.12306.cn/otn/login/userLogin'
        params = {
            '_json_att': '',
        }
        headers = {
            'User-Agent': FIREFOX_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
        }
        NetUtils.get(self.__session, url, params=params, headers=headers)

    def _uamtk(self):
        url = r'https://kyfw.12306.cn/passport/web/auth/uamtk'
        headers = {
            'Referer': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            'User-Agent': FIREFOX_USER_AGENT,
            'Connection': 'keep-alive',
        }
        response = NetUtils.post(self.__session, url, data={'appid': 'otn'}).json()

        def isSuccess(response):
            return response['result_code'] == 0 if 'result_code' in response else False

        return isSuccess(response), \
               response['result_message'] if 'result_message' in response else 'no result_message', \
               response['newapptk'] if 'newapptk' in response else 'no newapptk'

    def _uamauthclient(self, apptk):
        url = r'https://kyfw.12306.cn/otn/uamauthclient'
        headers = {
            'Referer': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            'User-Agent': FIREFOX_USER_AGENT,
            'Connection': 'keep-alive',
        }
        response = NetUtils.post(self.__session, url, data={'tk': apptk}, headers=headers)
        print(response.text)
        response = response.json()

        def isSuccess(response):
            return response['result_code'] == 0 if 'result_code' in response else False

        return isSuccess(response), '%s:%s' % (response['username'], response['result_message'])

    def login(self, userName, userPwd, type=TYPE_LOGIN_NORMAL_WAY):
        if type == TYPE_LOGIN_OTHER_WAY:
            return self._loginAsyncSuggest(userName, userPwd)
        return self._loginNormal(userName, userPwd)

    def _loginNormal(self, userName, userPwd):
        url = r'https://kyfw.12306.cn/passport/web/login'
        captcha = Captcha(self.__session)
        if not captcha.verifyCaptchaByHand()[1]:
            return False, '验证码识别错误!'
        headers = {
            'Referer': r'https://kyfw.12306.cn/otn/login/init',
            'User-Agent': FIREFOX_USER_AGENT,
            'Connection': 'keep-alive',
            'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
        }
        payload = {
            'username': userName,
            'password': userPwd,
            'appid': 'otn',
        }
        response = NetUtils.post(self.__session, url, data=payload, headers=headers)
        response = response.json() if response else None
        Log.v('loginResponse: %s' % response)

        def isLoginSuccess(responseJson):
            return 0 == responseJson['result_code'] if responseJson and 'result_code' in responseJson else False

        if not isLoginSuccess(response):
            return False
        self._passportRedirect()
        self._userLogin()
        result, msg, apptk = self._uamtk()
        if not Utils.check(result, msg):
            return False
        return self._uamauthclient(apptk)

    def _loginAsyncSuggest(self, userName, userPwd):
        captcha = Captcha(self.__session)
        results, verify = captcha.verifyCaptchaByHand(type=TYPE_LOGIN_OTHER_WAY)
        if not verify:
            return False, '验证码识别错误!'
        url = r'https://kyfw.12306.cn/otn/login/loginAysnSuggest'
        formData = {
            'loginUserDTO.user_name': userName,
            'userDTO.password': userPwd,
            'randCode': results,
        }
        headers = {
            'User-Agent': FIREFOX_USER_AGENT,
            'Referer': r'https://kyfw.12306.cn/otn/login/init',
            'Connection': 'keep-alive',
            'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
        }
        response = NetUtils.post(self.__session, url, data=formData, headers=headers)
        print('loginAsyncSuggest: %s' % response.text)
        response = response.json()

        def isSuccess(response):
            return response['status'] and response['data']['loginCheck'] == 'Y', response['data']['otherMsg']

        loginSuccess, otherMsg = isSuccess(response)
        return loginSuccess, '%s:%s' % (userName, otherMsg or '登录成功!')

    def isLogin(self):
        url = r'https://kyfw.12306.cn/otn/login/checkUser'
        headers = {
            'User-Agent': FIREFOX_USER_AGENT,
            'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
            'Connection': 'keep-alive',
        }
        formData = {
            '_json_att': ''
        }
        response = NetUtils.post(self.__session, url, formData, headers=headers)
        response = response.json() if response else None
        return response['data']['flag'] if response and 'data' in response and 'flag' in response[
            'data'] else False

    def logOut(self):
        self._loginOut()
        self._init()
        url = r'https://kyfw.12306.cn/passport/web/auth/uamtk'
        formData = {
            'appid': 'otn',
        }
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            # 'Content-Length': '9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
            'User-Agent': FIREFOX_USER_AGENT,
            'X-Requested-With': 'XMLHttpRequest',
            # 'Cookie':'_passport_session=3cae58f596b644f88b96ee8a448d9a737285; uamtk=7GdEj-S-9ZKfqcRkEjwCr6PLf4-SAiHRlY-wVm5sNnKizqTunx1210; RAIL_EXPIRATION=1515462916653; RAIL_DEVICEID=FH21u6JKmLVmsSwBvxOHIgRrgouY7azS3ENBUEL6aJKO9p3ou041Nv1QgAkLWHrWeeNJikYEgiZFKXUKXvaAJuRlxCN2sGDaKAkqZ2XKq8zhLtTpRZ8XcXkHXAdtirM4xzuuFesSAAWlg8gBZ37z_bF-N0VxtHo3; _jc_save_fromStation=%u6DF1%u5733%u5317%2CIOQ; _jc_save_toStation=%u6F6E%u6C55%2CCBQ; _jc_save_fromDate=2018-01-08; _jc_save_toDate=2018-01-08; _jc_save_showIns=true; _jc_save_wfdc_flag=dc; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=451936778.64545.0000; BIGipServerpool_passport=300745226.50215.0000'
        }
        response = NetUtils.post(self.__session, url, data=formData, headers=headers)
        # response = NetUtils.NormalPost(url, data=formData, headers=headers)
        pprint(response.request.headers)
        print(response.text)
        return response.json()

    def _loginOut(self):
        url = r'https://kyfw.12306.cn/otn/login/loginOut'
        headers = {
            'User-Agent': FIREFOX_USER_AGENT,
            'Referer': r'https://kyfw.12306.cn/otn/index/initMy12306',
            'Connection': 'keep-alive',
        }
        NetUtils.get(self.__session, url, headers=headers)

    def _init(self):
        url = r'https://kyfw.12306.cn/otn/login/init'
        headers = {
            'User-Agent': FIREFOX_USER_AGENT,
            'Referer': r'https://kyfw.12306.cn/otn/index/initMy12306',
            'Connection': 'keep-alive',
        }
        NetUtils.get(self.__session, url, headers=headers)


if __name__ == '__main__':
    pass
