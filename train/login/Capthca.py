from io import BytesIO

from PIL import Image

from define.Const import TYPE_LOGIN_NORMAL_WAY, TYPE_LOGIN_OTHER_WAY
from define.UrlsConf import loginUrls
from net.NetUtils import EasyHttp
from train.login import damatuWeb
from utils import FileUtils
from utils.Log import Log


class Captcha(object):
    __REPONSE_NORMAL_CDOE_SUCCESSFUL = '4'
    __REPONSE_OHTER_CDOE_SUCCESSFUL = '1'
    __CAPTCHA_PATH = 'captcha.jpg'

    def getCaptcha(self, type=TYPE_LOGIN_NORMAL_WAY):
        urlInfo = loginUrls['other']['captcha'] if type == TYPE_LOGIN_OTHER_WAY else loginUrls['normal']['captcha']
        print('catpchatImgURL: %s' % urlInfo['url'])
        return EasyHttp.send(urlInfo)

    def check(self, results, type=TYPE_LOGIN_NORMAL_WAY):
        if type == TYPE_LOGIN_OTHER_WAY:
            return self._checkRandCodeAnsyn(results)
        return self._captchaCheck(results)

    def _checkRandCodeAnsyn(self, results):
        formData = {
            'randCode': results,
            'rand': 'sjrand',
        }
        jsonRet = EasyHttp.send(loginUrls['other']['captchaCheck'], data=formData)
        print('checkRandCodeAnsyn: %s' %jsonRet)

        def verify(response):
            return response['status'] and Captcha.__REPONSE_OHTER_CDOE_SUCCESSFUL == response['data']['result']

        return verify(jsonRet)

    def _captchaCheck(self, results):
        data = {
            'answer': results,
            'login_site': 'E',
            'rand': 'sjrand',
        }
        jsonRet = EasyHttp.send(loginUrls['normal']['captchaCheck'], data=data)
        print('captchaCheck: %s' %jsonRet)

        def verify(response):
            return Captcha.__REPONSE_NORMAL_CDOE_SUCCESSFUL == response[
                'result_code'] if 'result_code' in response else False

        return verify(jsonRet)

    def verifyCaptchaByClound(self, type=TYPE_LOGIN_NORMAL_WAY):
        captchaContent = self.getCaptcha(type)
        if captchaContent:
            FileUtils.saveBinary(Captcha.__CAPTCHA_PATH, captchaContent)
        else:
            Log.e('failed to save captcha')
            return None
        results = damatuWeb.verify(Captcha.__CAPTCHA_PATH)
        results = self.__cloundTransCaptchaResults(results)
        Log.v('captchaResult: %s' % results)
        return results, self.check(results)

    def verifyCaptchaByHand(self, type=TYPE_LOGIN_NORMAL_WAY):
        img = Image.open(BytesIO(self.getCaptcha(type)))
        img.show()
        Log.v(
            """ 
            -----------------
            | 0 | 1 | 2 | 3 |
            -----------------
            | 4 | 5 | 6 | 7 |
            ----------------- """)
        results = input("输入验证码索引(见上图，以','分割）: ")
        img.close()
        results = self.__indexTransCaptchaResults(results)
        Log.v('captchaResult: %s' % results)
        return results, self.check(results, type)

    def __indexTransCaptchaResults(self, indexes, sep=r','):
        coordinates = ['40,40', '110,40', '180,40', '250,40', '40,110', '110,110', '180,110', '250,110']
        results = []
        for index in indexes.split(sep=sep):
            results.append(coordinates[int(index)])
        return ','.join(results)

    def __cloundTransCaptchaResults(self, results):
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

