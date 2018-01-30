import random

loginUrls = {
    'normal': {
        'init': {
            'url': r'https://kyfw.12306.cn/otn/login/init',
            'method': 'GET',
            'headers': {
                'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Referer': r'https://kyfw.12306.cn/otn/index/initMy12306',
            }
        },
        'uamtk': {
            'url': r'https://kyfw.12306.cn/passport/web/auth/uamtk',
            'method': 'POST',
            'headers': {
                r'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            }
        },
        'captcha': {
            'url': r'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&{}'
                .format(random.random()),
            'method': 'GET',
            'response': 'binary',
        },
        'captchaCheck': {
            'url': r'https://kyfw.12306.cn/passport/captcha/captcha-check',
            'method': 'POST',
            'headers': {
                'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': r'https://kyfw.12306.cn/otn/login/init',
            }
        },
        'login': {
            'url': r'https://kyfw.12306.cn/passport/web/login',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'X-Requested-With': 'xmlHttpRequest',
                'Referer': 'https://kyfw.12306.cn/otn/login/init',
            }
        },
        'userLogin': {
            'url': r'https://kyfw.12306.cn/otn/login/userLogin',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://kyfw.12306.cn/otn/login/init',
            }
        },
        'userLoginRedirect': {
            'url': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            'method': 'GET',
        },
        'uamauthclient': {
            'url': r'https://kyfw.12306.cn/otn/uamauthclient',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            }
        },
        'checkUser': {
            'url': r'https://kyfw.12306.cn/otn/login/checkUser',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
            }
        },
        'loginOut': {
            'url': r'https://kyfw.12306.cn/otn/login/loginOut',
            'method': 'GET',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/index/initMy12306',
            }
        },

    },
    # --------------------------------------------------------------------------------------------------------
    'other': {
        'init': {
            'url': r'https://kyfw.12306.cn/otn/login/init',
            'method': 'GET',
            'headers': {
                'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                r'Content-Type': r'application/x-www-form-urlencoded',
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
            }
        },
        'uamtk': {
            'url': r'https://kyfw.12306.cn/passport/web/auth/uamtk',
            'method': 'POST',
            'headers': {
                r'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            }
        },
        'captcha': {
            'url': r'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&rand=sjrand&{}'
                .format(random.random()),
            'method': 'GET',
            'response': 'binary',
        },
        'captchaCheck': {
            'url': r'https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn',
            'method': 'POST',
            'headers': {
                'Origin': r'https://kyfw.12306.cn',
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
                'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
            }
        },
        'login': {
            'url': r'https://kyfw.12306.cn/otn/login/loginAysnSuggest',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'Origin': r'https://kyfw.12306.cn',
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
            }
        },
        'loginOut': {
            'url': r'https://kyfw.12306.cn/otn/login/loginOut',
            'method': 'GET',
            'headers': {
                r'Content-Type': r'application/x-www-form-urlencoded',
                'Host': r'kyfw.12306.cn',
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
            }
        },
    },
}

queryUrls = {
    'query': {
        'url': r'https://kyfw.12306.cn/otn/leftTicket/queryZ',
        'method': 'GET',
        'headers': {
            'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
        }
    },
}
submitUrls = {
    'dc': {
        'submitOrderRequest': {
            'url': r'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest',
            'method': 'POST',
            'headers': {
                'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
                'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': r'kyfw.12306.cn',
            },
        },
        'getPassengerDTOs': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs',
            'method': 'POST',
        },
        'getExtraInfo': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'method': 'GET',
            'response': 'html',
        },
        'checkOrderInfo': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            },
        },
        'getQueueCount': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            },
        },
        'confirmForQueue': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
        },
        'queryOrderWaitTime': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime',
            'method': 'GET',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            },
        },
        'resultOrderForQueue': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            },
        },

    },
    'wc': {
        'submitOrderRequest': {
            'url': r'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest',
            'method': 'POST',
            'headers': {
                'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
                'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': r'kyfw.12306.cn',
            },
        },
        'getPassengerDTOs': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs',
            'method': 'POST',
        },
        'getExtraInfo': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
            'method': 'GET',
            'response': 'html',
        },
        'checkOrderInfo': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
            },
        },
        'getQueueCount': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
            },
        },
        'confirmForQueue': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/confirmGoForQueue',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
        },
        'queryOrderWaitTime': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime',
            'method': 'GET',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
            },
        },
        'resultOrderForQueue': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForWcQueue',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
            },
        },

    }
}
