# seatType:商务座(9),特等座(P),一等座(M),二等座(O),高级软卧(6),软卧(4),硬卧(3),软座(2),硬座(1),无座(1)
# ticket_type_codes:ticketInfoForPassengerForm['limitBuySeatTicketDTO']['ticket_type_codes']:(成人票:1,儿童票:2,学生票:3,残军票:4)
import urllib

from define.Const import SEAT_TYPE, SeatName, PASSENGER_TICKET_TYPE_CODE_TO_DESC


# O,0,1,name,1,identity,phone,N_O,0,1,name2,1,identity2,phone2,N
def passengerTicketStrs(seatType, passengersDetails, ticketTypeCodes=1):
    if not isinstance(passengersDetails, list):
        return passengerTicketStr(seatType, passengersDetails, ticketTypeCodes)
    return '_'.join(passengerTicketStr(seatType, passenger, ticketTypeCodes) for passenger in passengersDetails)


def passengerTicketStr(seatType, passengerDetails, ticketTypeCodes=1):
    # 1(seatType),0,1(车票类型:ticket_type_codes),张三(passenger_name),1(证件类型:passenger_id_type_code),320xxxxxx(passenger_id_no),151xxxx(mobile_no),N
    return '%s,0,%s,%s,%s,%s,%s,N' % (seatType,
                                      ticketTypeCodes,
                                      passengerDetails.passengerName,
                                      passengerDetails.passengerIdTypeCode,
                                      passengerDetails.passengerIdNo,
                                      passengerDetails.mobileNo)


# name,1,identity,1_name2,1,identity2,1_
def oldPassengerStrs(passengersDetails):
    if not isinstance(passengersDetails, list):
        return oldPassengerStr(passengersDetails)
    return ''.join([oldPassengerStr(passenger) for passenger in passengersDetails])


def oldPassengerStr(passengerDetails):
    # oldPassengerStr-->张三(passenger_name),1(证件类型:passenger_id_type_code),320xxxxxx(passenger_id_no),1_
    return '%s,%s,%s,1_' % (passengerDetails.passengerName,
                            passengerDetails.passengerIdTypeCode,
                            passengerDetails.passengerIdNo)


def undecodeSecretStr(urlDecodedSecretStr):
    return urllib.parse.unquote(urlDecodedSecretStr).replace('\n', '')


def seatWhich(seatTypes, ticketDetails):
    for seatCode in seatTypes:
        if seatCode == SEAT_TYPE[SeatName.BUSINESS_SEAT]:
            yield SeatName.BUSINESS_SEAT, ticketDetails.businessSeat
            continue
        if seatCode == SEAT_TYPE[SeatName.SPECIAL_SEAT]:
            yield SeatName.BUSINESS_SEAT, ticketDetails.businessSeat
            continue
        if seatCode == SEAT_TYPE[SeatName.FIRST_CLASS_SEAT]:
            yield SeatName.FIRST_CLASS_SEAT, ticketDetails.firstClassSeat
            continue
        if seatCode == SEAT_TYPE[SeatName.SECOND_CLASS_SEAT]:
            yield SeatName.SECOND_CLASS_SEAT, ticketDetails.secondClassSeat
            continue
        if seatCode == SEAT_TYPE[SeatName.ADVANCED_SOFT_SLEEP]:
            yield SeatName.ADVANCED_SOFT_SLEEP, ticketDetails.advancedSoftSleep
            continue
        if seatCode == SEAT_TYPE[SeatName.SOFT_SLEEP]:
            yield SeatName.SOFT_SLEEP, ticketDetails.softSleep
            continue
        if seatCode == SEAT_TYPE[SeatName.HARD_SLEEP]:
            yield SeatName.HARD_SLEEP, ticketDetails.hardSleep
            continue
        if seatCode == SEAT_TYPE[SeatName.SOFT_SEAT]:
            yield SeatName.SOFT_SEAT, ticketDetails.softSeat
            continue
        if seatCode == SEAT_TYPE[SeatName.HARD_SEAT]:
            yield SeatName.HARD_SEAT, ticketDetails.hardSeat
            continue
        if seatCode == SEAT_TYPE[SeatName.NO_SEAT]:
            yield SeatName.NO_SEAT, ticketDetails.noSeat
            continue


def passengerType2Desc(passengerTypeCode):
    return PASSENGER_TICKET_TYPE_CODE_TO_DESC.get(passengerTypeCode)
