from datetime import datetime
import traceback

import requests

from define.Const import SEAT_TYPE, PASSENGER_TICKET_TYPE_CODES, TourFlag
from train.login.Login import Login
from train.query.Query import Query
from train.submit.Submit import Submit
from utils import TrainUtils
from utils import Utils
from utils.Log import Log

if __name__ == '__main__':
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    # 禁用安全请求警告
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    userName = input('请输入用户名:').strip()
    userPwd = input('请输入密码:').strip()
    trainDate = input('请输入乘车日期（YYYY-mm-dd): ').strip() or datetime.now().strftime('%Y-%m-%d')
    fromStation = input('请输入出发站:').strip() or '深圳北'
    toStation = input('请输入到达站:').strip() or '潮汕'
    seatTypes = input('请输入座位类别(多个以,分隔,默认:所有)%s: ' % (['%s:%s' % (seat, code) for seat, code in SEAT_TYPE.items()])
                      ).strip().split(',')
    seatTypesCode = seatTypes if seatTypes[0] else [SEAT_TYPE[key] for key in SEAT_TYPE.keys()]
    passengerTypeCode = input('请输入购票类型(默认:成人）:%s:' % (
        ['%s:%s' % (name, code) for name, code in PASSENGER_TICKET_TYPE_CODES.items()])).strip() or '1'
    passengersId = input('请输入乘客身份证号(多个以,分隔): ').strip().split(',')
    tourFlag = input(
        '单程:%s,往返:%s(默认%s): ' % (TourFlag.SINGLE, TourFlag.GO_BACK, TourFlag.SINGLE)).strip() or TourFlag.SINGLE
    Log.d('出发日期: %s,座位类别: %s,乘客类型: %s,车票类型: %s' % (trainDate, seatTypesCode, passengerTypeCode, tourFlag))

    session = requests.session()

    login = Login(session)
    for count in range(1, 10, 1):
        Log.v('[%d]正在进行登录...' % count)
        result, msg = login.login(userName, userPwd, type=(count - 1) % 2)
        if Utils.check(result, msg):
            break
        Log.w('登录失败，正在重新进行登录...')
    if not Utils.check(login.isLogin(), '登录失败,程序退出!'):
        exit(-1)
    Log.v('%s,登录成功' % msg)
    ticketDetails = Query.loopQuery(session, trainDate, fromStation, toStation,
                                    TrainUtils.passengerType2Desc(passengerTypeCode), seatTypesCode)
    if not Utils.check(ticketDetails, '刷票失败!'):
        exit(-1)
    Log.v('已为您查询到可用余票:%s' % ticketDetails)

    ticketDetails.passengersId = passengersId
    ticketDetails.ticketTypeCodes = passengerTypeCode
    ticketDetails.tourFlag = tourFlag
    submit = Submit(session, ticketDetails)
    try:
        submit.submit()
    except Exception as e:
        Log.w('exception occured!')
        traceback.print_exc()
    finally:
        login.logOut()
