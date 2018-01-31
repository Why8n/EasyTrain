from Configure import *
from define.Const import SEAT_TYPE
from train.login.Login import Login
from train.query.Query import Query
from train.submit.Submit import Submit
from utils import TrainUtils
from utils import Utils
from utils.Log import Log


def main():
    login = Login()
    Log.v('正在登录...')
    result, msg = login.login(USER_NAME, USER_PWD)
    if not Utils.check(result, msg):
        Log.e(msg)
        return
    Log.v('%s,登录成功' % msg)

    seatTypesCode = SEAT_TYPE_CODE if SEAT_TYPE_CODE else [SEAT_TYPE[key] for key in SEAT_TYPE.keys()]
    passengerTypeCode = PASSENGER_TYPE_CODE if PASSENGER_TYPE_CODE else '1'
    while True:
        # 死循环一直查票，直到下单成功
        try:
            print('-' * 40)
            ticketDetails = Query.loopQuery(TRAIN_DATE, FROM_STATION, TO_STATION,
                                            TrainUtils.passengerType2Desc(passengerTypeCode), seatTypesCode)
            Log.v('已为您查询到可用余票:%s' % ticketDetails)

            ticketDetails.passengersId = PASSENGERS_ID
            ticketDetails.ticketTypeCodes = passengerTypeCode
            ticketDetails.tourFlag = TOUR_FLAG if TOUR_FLAG else 'dc'
            submit = Submit(ticketDetails)
            if submit.submit():
                submit.showSubmitInfoPretty()
                break
        except Exception as e:
            Log.w('exception occured,now retrying...')
            # traceback.print_exc()
    print(login.loginOut())


if __name__ == '__main__':
    main()
