import requests
import base64

KEYS = {}


def validate_response(rakuten_response):
    if rakuten_response.status_code == 200:
        return rakuten_response.json()
    else:
        return error(rakuten_response.json())


def authentication_key(document=None, api_key=None):
    global KEYS
    data = f'{document}:{api_key}'
    b64 = base64.b64encode(data.encode("utf-8"))
    KEYS['api_key'] = b64.decode("utf-8")
    return KEYS


def delete(end_point, data={}):
    rakuten_response = requests.delete(end_point, json=data, headers=headers())
    return validate_response(rakuten_response)


def get(end_point, data={}):
    rakuten_response = requests.get(end_point, json=data, headers=headers())
    return validate_response(rakuten_response)


def post(end_point, data={}):
    rakuten_response = requests.post(end_point, json=data, headers=headers())
    return validate_response(rakuten_response)


def put(end_point, data={}):
    rakuten_response = requests.put(end_point, json=data, headers=headers())
    return validate_response(rakuten_response)


def error(data):
    raise Exception(data['errors'])


def headers():
    _headers = {'content-type': 'application/json', 'Authorization': 'Basic %s' % KEYS["api_key"]}
    return _headers
