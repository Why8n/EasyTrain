"""
下单
"""
import json
import re
import time
from datetime import datetime

from define.Const import TourFlag
from define.UserAgent import FIREFOX_USER_AGENT
from net import NetUtils
from train.submit.PassengerDetails import PassengerDetails
from utils import TrainUtils
from utils import Utils
from utils.Log import Log


class Submit(object):
    def __init__(self, session, ticketDetails):
        self.__session = session
        self.__ticket = ticketDetails

    # submit orher request,check if the orher is qualified
    def _submitOrderRequest(self, tourFlag='dc'):
        url = r'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        headers = {
            'User-Agent': FIREFOX_USER_AGENT,
            # 'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init?random={}'.format(time.time() * 1000),
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'Accept': r'*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            # 'Content-Length':'444',
            'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': r'kyfw.12306.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'Cache-Control': 'no-cache',
            'If-Modified-Since': '0',
        }
        formData = {
            'secretStr': TrainUtils.undecodeSecretStr(self.__ticket.secretStr),
            # 'secretStr': self.__ticket.secretStr,
            # 'secretStr': urllib.parse.unquote(self.__ticket.secretStr),
            'train_date': Utils.formatDate(self.__ticket.startDate),  # 2018-01-04
            # todo::check time style
            'back_train_date': time.strftime("%Y-%m-%d", time.localtime()),  # query date:2017-12-31
            'tour_flag': tourFlag,
            'purpose_codes': self.__ticket.passengerType,
            'query_from_station_name': self.__ticket.fromStation,
            'query_to_station_name': self.__ticket.toStation,
            'undefined': '',
        }
        response = self.__session.post(url, formData, headers=headers)
        # response = NetUtil.post(self.__session, url, formData, headers=headers)
        print(response.text)
        response = response.json()
        result = response['status'] if 'status' in response else False
        msg = response['messages'] if 'messages' in response else None  # list type
        return result, msg

    def _getExtraInfo(self):
        url = r'https://kyfw.12306.cn/otn/confirmPassenger/{}'.format(
            '%s' % ('initWc' if self.__ticket.tourFlag == TourFlag.GO_BACK else 'initDc'))
        print(url)

        def getRepeatSubmitToken(html):
            repeatSubmitToken = re.findall(r"var globalRepeatSubmitToken = '(.*)'", html)[0]
            print('RepeatSubmitToken = %s' % repeatSubmitToken)
            return repeatSubmitToken

        html = NetUtils.get(self.__session, url,
                            headers={'User-Agent': FIREFOX_USER_AGENT, 'Connection': 'keep-alive', }).text
        # print('getExtraInfo', html)
        self.__ticket.repeatSubmitToken = getRepeatSubmitToken(html)

        def decodeTicketInfoForPassengerForm(html):
            ticketInfoForPassengerForm = re.findall(r'var ticketInfoForPassengerForm=(.*);', html)[0]
            return json.loads(ticketInfoForPassengerForm.replace("'", "\""))

        self.__ticket.ticketInfoForPassengerForm = decodeTicketInfoForPassengerForm(html)

    def __getPassengerInfo(self, passengersList):
        passengersDetails = {}
        for passengerJson in passengersList:
            passenger = PassengerDetails()
            passenger.passengerName = passengerJson['passenger_name'] or ''
            passenger.code = passengerJson['code'] or ''
            passenger.sexCode = passengerJson['sex_code'] or ''
            passenger.sexName = passengerJson['sex_name'] or ''
            passenger.bornDate = passengerJson['born_date'] or ''
            passenger.countryCode = passengerJson['country_code'] or ''
            passenger.passengerIdTypeCode = passengerJson['passenger_id_type_code'] or ''
            passenger.passengerIdTypeName = passengerJson['passenger_id_type_name'] or ''
            passenger.passengerIdNo = passengerJson['passenger_id_no'] or ''
            passenger.passengerType = passengerJson['passenger_type'] or ''
            passenger.passengerFlag = passengerJson['passenger_flag'] or ''
            passenger.passengerTypeName = passengerJson['passenger_type_name'] or ''
            passenger.mobileNo = passengerJson['mobile_no'] or ''
            passenger.phoneNo = passengerJson['phone_no'] or ''
            passenger.email = passengerJson['email'] or ''
            passenger.address = passengerJson['address'] or ''
            passenger.postalcode = passengerJson['postalcode'] or ''
            passenger.firstLetter = passengerJson['first_letter'] or ''
            passenger.recordCount = passengerJson['recordCount'] or ''
            passenger.totalTimes = passengerJson['total_times'] or ''
            passenger.indexId = passengerJson['index_id'] or ''
            passengersDetails[passenger.passengerIdNo] = passenger
        return passengersDetails

    # get user's passengers info
    def _getPassengerDTOs(self):
        self._getExtraInfo()
        url = r'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        formData = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        response = NetUtils.post(self.__session, url, data=formData,
                                 headers={'User-Agent': FIREFOX_USER_AGENT, 'Connection': 'keep-alive', }).json()
        passengersList = response['data']['normal_passengers']
        return response['status'] if 'status' in response else False, \
               response['messages'] if 'messages' in response else '无法获取乘客信心，请先进行添加!', \
               self.__getPassengerInfo(passengersList)

    # passengerName:乘客姓名
    # seatType:座位类别（一等座，二等座····）
    # ticketTypeCodes:车票类别代码
    def _checkOrderInfo(self, passengersDetails, seatType, ticketTypeCodes=1):
        url = r'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        # self.__ticket.seatType = seatType
        # self.__ticket.ticketTypeCodes = ticketTypeCodes
        # self.passengerDetails = passengerDetails
        formData = {
            'cancel_flag': self.__ticket.ticketInfoForPassengerForm['orderRequestDTO']['cancel_flag'] or '2',
            'bed_level_order_num': self.__ticket.ticketInfoForPassengerForm['orderRequestDTO'][
                                       'bed_level_order_num'] or '000000000000000000000000000000',
            'passengerTicketStr': TrainUtils.passengerTicketStrs(seatType, passengersDetails, ticketTypeCodes),
            'oldPassengerStr': TrainUtils.oldPassengerStrs(passengersDetails),
            'tour_flag': self.__ticket.ticketInfoForPassengerForm['tour_flag'] or 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        headers = {
            'User-Agent': FIREFOX_USER_AGENT,
            'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'Connection': 'keep-alive',
        }
        response = NetUtils.post(self.__session, url, formData, headers=headers).json()
        return response['status'], response['messages'], response['data']['submitStatus'], \
               response['data']['errMsg'] if 'errMsg' in response['data'] else 'submit falied'

    def _getQueueCount(self):
        url = r'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        formData = {
            # Thu+Jan+04+2018+00:00:00+GMT+0800
            # 'train_date': datetime.strptime(
            #     self.__ticket.ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['train_date'], '%Y%m%d').strftime(
            #     '%b+%a+%d+%Y+00:00:00+GMT+0800'),
            # Mon Jan 08 2018 00:00:00 GMT+0800 (中国标准时间)
            'train_date': datetime.strptime(
                self.__ticket.ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['train_date'], '%Y%m%d').strftime(
                '%b %a %d %Y 00:00:00 GMT+0800') + ' (中国标准时间)',
            'train_no': self.__ticket.ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['train_no'],
            'stationTrainCode': self.__ticket.trainNo,
            'seatType': self.__ticket.seatType,
            'fromStationTelecode': self.__ticket.fromStationCode,
            'toStationTelecode': self.__ticket.toStationCode,
            'leftTicket': self.__ticket.ticketInfoForPassengerForm['leftTicketStr'],
            'purpose_codes': self.__ticket.ticketInfoForPassengerForm['purpose_codes'],
            'train_location': self.__ticket.ticketInfoForPassengerForm['train_location'],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        headers = {
            'User-Agent': FIREFOX_USER_AGENT,
            'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'Connection': 'keep-alive',
        }
        response = NetUtils.post(self.__session, url, data=formData, headers=headers).json()
        return response['status'], response['messages'], \
               response['data']['ticket'] if 'data' in response and 'ticket' in response['data'] else -1, \
               response['data']['count'] if 'data' in response and 'count' in response['data'] else -1

    # network busy usually occured
    def _confirmSingleOrGoForQueue(self, passengersDetails):
        url = r'https://kyfw.12306.cn/otn/confirmPassenger/confirmGoForQueue' if self.__ticket.tourFlag == TourFlag.GO_BACK \
            else r'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        formData = {
            'passengerTicketStr': TrainUtils.passengerTicketStrs(self.__ticket.seatType, passengersDetails,
                                                                 self.__ticket.ticketTypeCodes),
            'oldPassengerStr': TrainUtils.oldPassengerStrs(passengersDetails),
            'randCode': '',
            'purpose_codes': self.__ticket.ticketInfoForPassengerForm['purpose_codes'],
            'key_check_isChange': self.__ticket.ticketInfoForPassengerForm['key_check_isChange'],
            'leftTicketStr': self.__ticket.ticketInfoForPassengerForm['leftTicketStr'],
            'train_location': self.__ticket.ticketInfoForPassengerForm['train_location'],
            'choose_seats': '',  # todo::how to choose seats
            'seatDetailType': '000',  # todo::make clear 000 comes from
            'whatsSelect': '1',
            'roomType': '00',  # todo::make clear this value comes from
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        headers = {
            'User-Agent': FIREFOX_USER_AGENT,
            'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/{}'.format(
                'initWc' if self.__ticket.tourFlag == TourFlag.GO_BACK else 'initDc'),
            'Connection': 'keep-alive',
            r'Accept': r'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'kyfw.12306.cn',
            'X-Requested-With': 'XMLHttpRequest',
        }
        response = NetUtils.post(self.__session, url, data=formData, headers=headers).json()
        return response['status'], response['messages'], response['data']['submitStatus'], response['data'][
            'errMsg'] if 'errMsg' in response['data'] else None

    def _queryOrderWaitTime(self):
        url = r'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime'
        params = {
            'random': '%10d' % (time.time() * 1000),
            'tourFlag': self.__ticket.ticketInfoForPassengerForm['tour_flag'] or 'dc',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        headers = {
            'User-Agent': FIREFOX_USER_AGENT,
            'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'Connection': 'keep-alive',
        }
        response = NetUtils.get(self.__session, url, params=params, headers=headers).json()
        print('queryOrderWaitTime: %s' % response)
        return response['status'], response['messages'], response['data']['waitTime'], response['data']['orderId'], \
               response['data']['msg'] if 'msg' in response['data'] else None

    def _resultOrderForDcOrWcQueue(self, orderSequenceNo):
        url = r'https://kyfw.12306.cn/otn/confirmPassenger/{}'.format(
            'resultOrderForWcQueue' if self.__ticket.tourFlag == TourFlag.GO_BACK else 'resultOrderForDcQueue')
        formData = {
            'orderSequence_no': orderSequenceNo,
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        headers = {
            'User-Agent': FIREFOX_USER_AGENT,
            'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'Connection': 'keep-alive',
        }
        response = NetUtils.post(self.__session, url, data=formData, headers=headers)
        print('resultOrderForDcOrWcQueue', response.text)
        response = response.json()
        return response['status'], response['messages'], response['data']['submitStatus']

    def _payOrderInfo(self):
        url = r'https://kyfw.12306.cn/otn//payOrder/init?random=%10d' % (time.time() * 1000)
        headers = {
            'User-Agent': FIREFOX_USER_AGENT,
            'Connection': 'keep-alive',
        }
        response = NetUtils.get(self.__session, url, headers=headers).text

    # seatType:商务座(9),特等座(P),一等座(M),二等座(O),高级软卧(6),软卧(4),硬卧(3),软座(2),硬座(1),无座(1)
    # ticket_type_codes:ticketInfoForPassengerForm['limitBuySeatTicketDTO']['ticket_type_codes']:(成人票:1,儿童票:2,学生票:3,残军票:4)
    def submit(self):
        status, msg = self._submitOrderRequest(self.__ticket.tourFlag)
        if not Utils.check(status, 'submitOrderRequesst: %s' % msg):
            return
        Log.v('提交订单请求成功!')

        status, msg, passengersDetailsList = self._getPassengerDTOs()
        if not Utils.check(status, 'getPassengerDTOs: %s' % msg):
            return
        Log.v('获取乘客信息成功!')

        passengersDetails = []
        for id in self.__ticket.passengersId:
            passengersDetails.append(passengersDetailsList.get(id))

        status, msg, submitStatus, errMsg = self._checkOrderInfo(passengersDetails, self.__ticket.seatType,
                                                                 self.__ticket.ticketTypeCodes)
        if not Utils.check(status, 'checkOrderInfo: %s' % msg) or not Utils.check(submitStatus,
                                                                                  'checkOrderInfo: %s' % errMsg):
            return
        Log.v('校验订单信息成功!')

        status, msg, leftTickets, personsCount = self._getQueueCount()
        if not Utils.check(status, 'getQueueCount: %s' % msg):
            return
        Log.v('%s 剩余车票:%s ,目前排队人数: %s' % (self.__ticket.trainNo, leftTickets, personsCount))
        status, msg, submitStatus, errMsg = self._confirmSingleOrGoForQueue(passengersDetails)
        if not Utils.check(status, 'confirmSingleOrGoForQueue: %s' % msg) \
                or not Utils.check(submitStatus, 'confirmSingleOrGoForQueue: %s' % errMsg or '订单信息提交失败！'):
            return

        orderId = self.__waitForOrderId()
        if not Utils.check(orderId, '订单获取失败！'):
            return

        status, msg, submitStatus = self._resultOrderForDcOrWcQueue(orderId)
        if not Utils.check(status, 'resultOrderForDcOrWcQueue: %s' % msg):
            return
        if not submitStatus:
            Log.e('订单提交失败！')
            return
        Log.v('您已成功订购火车票！请在30分钟内前往12306官方网站进行支付！')

    def __waitForOrderId(self):
        Log.v('正在排队获取订单!')
        count = 0
        while True:
            count += 1
            status, msg, waitTime, orderId, errorMsg = self._queryOrderWaitTime()
            if not Utils.check(status, 'queryOrderWaitTime: %s' % msg):
                return None
            Log.v('[%d]正在等待订单提交结果...' % count)
            if waitTime < 0:
                if orderId:
                    Log.v('订单提交成功，订单号: %s' % orderId)
                    return orderId
                elif errorMsg:
                    Log.v(errorMsg)
                    return None
            Log.w('订单提交正在入队...')
            time.sleep(3)
        return None
