import requests
from utils.Log import Log


def normalGet(url, params=None, **kwargs):
    try:
        response = requests.get(url, params=params, **kwargs)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except:
        Log.e('can not visit url: ' + url)
        return None


def get(session, url, **kwargs):
    try:
        response = session.get(url, **kwargs)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except:
        Log.e('can not visit url: ' + url)
        raise
        return None


def NormalPost(url, data=None, json=None, **kwargs):
    try:
        response = requests.post(url, data, json, **kwargs)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except:
        Log.e('can not visit url: ' + url)
        return None


def post(session, url, data=None, json=None, **kwargs):
    try:
        response = session.post(url, data, json, **kwargs)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except:
        Log.e('can not visit url: ' + url)
        return None
