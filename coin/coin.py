import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import json
import requests
import pyupbit

#lib
from libary import tickerInfo

# GUI
from gui import textBox

access_key =  os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key =  os.environ['UPBIT_OPEN_API_SECRET_KEY']
server_url = 'https://api.upbit.com'  # os.environ['UPBIT_OPEN_API_SERVER_URL']

def accountsInquiry():
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/accounts", headers=headers)
    return res.json()

def allOrderListINquiry():
    query = {
        'state': 'done',
    }
    query_string = urlencode(query)

    uuids = [
        '9ca023a5-851b-4fec-9f0a-48cd83c2eaae',
    ]
    uuids_query_string = '&'.join(["uuids[]={}".format(uuid) for uuid in uuids])

    query['uuids[]'] = uuids
    query_string = "{0}&{1}".format(query_string, uuids_query_string).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/orders", params=query, headers=headers)
    json_data = res.json()
    resultString = json.dumps(json_data, indent="\n")
    print(resultString)
    return resultString

def singleOrdersInquiry(marketKey = 'KRW-BTC'):
    query = {
        'market': marketKey,
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/orders/chance", params=query, headers=headers)
    json_data = res.json()
    resultString = json.dumps(json_data, indent="\n")
    print(resultString)
    return resultString

def middleCandle():
    url = "https://api.upbit.com/v1/candles/minutes/1"

    querystring = {
        "market": "KRW-XRP"
        , "to": "2021-05-11 02:14:11"
        , "count": "1"
        }

    response = requests.request("GET", url, params=querystring)
    json_data = response.text
    resultString = json.dumps(json_data, indent="\n")
    print(resultString)
    return resultString

def walletHistory():
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }
    print("uid : " + payload.get('nonce') + "\n")

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/status/wallet", headers=headers)
    json_data = res.text
    resultString = json.dumps(json_data, indent="\n")
    print(resultString)
    return resultString

def keyInfo():
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/api_keys", headers=headers)

    resultString = json.dumps(json_data, indent="\n")
    print(resultString)
    return resultString



# 여기부터 사용

# 코인 현재가 보는 프로그램
def currentCoinPriceInfo(markets):
    url = "https://api.upbit.com/v1/ticker"
    headers = {"Accept": "application/json"}
    querystring = {"markets":markets}
    response = requests.request("GET", url, headers=headers,  params=querystring)
    return response


if __name__ == '__main__':  # 프로그램의 시작점일 때만 아래 코드 실행
    
    allOrderListINquiry()

   # tickerInfoList = tickerInfo.getTickInfo()
   # 
   # datas = accountsInquiry()
   # print("============ strt ============\n\n")
   # for data in datas:
   #     key = data['unit_currency'] + '-' + data['currency']
   #     print(data)
   # print("============ end ============\n\n")

    # singleOrdersInquiry()
    # middleCandle()
    # walletHistory()
    # keyInfo()
    # price = pyupbit.get_current_price("KRW-XRP")
    # print(price)