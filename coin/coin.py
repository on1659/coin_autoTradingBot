import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import json
import requests
import pyupbit
import time

#lib
from libary import tickerInfo

# GUI
from gui import textBox

access_key =  os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key =  os.environ['UPBIT_OPEN_API_SECRET_KEY']


access_key_all =  os.environ['UPBIT_OPEN_API_ACCESS_KEY_ALL']
secret_key_all =  os.environ['UPBIT_OPEN_API_SECRET_KEY_ALL']

server_url = 'https://api.upbit.com'  # os.environ['UPBIT_OPEN_API_SERVER_URL']

global gRequestCount
global lastOrderTime
global secInterval

gRequestCount = 0
secInterval = 0.0
lastOrderTime = time.time()

def consleconslePrint(msg):
    print(msg)
    return;

def timestamp():
   #return
    global gRequestCount
    global lastOrderTime
    global secInterval
    
    
    interval = time.time() - lastOrderTime;
    secInterval = float(secInterval) + float(interval)
    gRequestCount = gRequestCount + 1
    
    if secInterval > 1:
        consleconslePrint("request : " + str(gRequestCount))
        gRequestCount = 0
        secInterval = 0
    
    # consleconslePrint("request : " + str(gRequestCount) + " - interval : " + str(interval))
    lastOrderTime = time.time()
    return

def accountsInquiry():
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/accounts", headers=headers)
   
    timestamp()
    return res.json()

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
    conslePrint(resultString)

    timestamp()
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
    conslePrint(resultString)
    
    timestamp()
    return resultString

def walletHistory():
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }
    conslePrint("uid : " + payload.get('nonce') + "\n")

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/status/wallet", headers=headers)
    json_data = res.text
    resultString = json.dumps(json_data, indent="\n")
    conslePrint(resultString)
    
    timestamp()
    return resultString

# 여기부터 사용

# 코인 현재가 보는 프로그램
def currentCoinPriceInfo(markets):
    url = "https://api.upbit.com/v1/ticker"
    headers = {"Accept": "application/json"}
    querystring = {"markets":markets}
    response = requests.request("GET", url, headers=headers,  params=querystring)
    
    timestamp()
    return response



# 주문가능 정보 조회
def orderChance(markets):
    query = {'market': markets }
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
    response = requests.get(server_url + "/v1/orders/chance", params=query, headers=headers)
    
    timestamp()
    return response

def ordersListInquiry():
  #    query = {
  #      'state': 'done',
  #  }
  #  query_string = urlencode(query)
  #
  #  query['uuids[]'] = uuids
  #  query_string = "{0}&{1}".format(query_string, uuids_query_string).encode()
  #
  #  m = hashlib.sha512()
  #  m.update(query_string)
  #  query_hash = m.hexdigest()
  #
  #  payload = {
  #      'access_key': access_key,
  #      'nonce': str(uuid.uuid4()),
  #      'query_hash': query_hash,
  #      'query_hash_alg': 'SHA512',
  #  }
  #
  #  jwt_token = jwt.encode(payload, secret_key)
  #  authorize_token = 'Bearer {}'.format(jwt_token)
  #  headers = {"Authorization": authorize_token}
  #
  #  res = requests.get(server_url + "/v1/orders", params=query, headers=headers)
    return

def order():
    query = {
    'market': 'KRW-XRP',
    'side': 'bid',
    'volume': '5',
    'price': '1335.0',
    'ord_type': 'limit',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key_all,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key_all)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
    
    timestamp()
    return

def requestCandles(markets, min = 1):
    url = "https://api.upbit.com/v1/candles/minutes/1"
    querystring = {"market":markets, "count":str(min)}
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response



if __name__ == '__main__':  # 프로그램의 시작점일 때만 아래 코드 실행
    
    allOrderListINquiry()

   # tickerInfoList = tickerInfo.getTickInfo()
   # 
   # datas = accountsInquiry()
   # conslePrint("============ strt ============\n\n")
   # for data in datas:
   #     key = data['unit_currency'] + '-' + data['currency']
   #     conslePrint(data)
   # conslePrint("============ end ============\n\n")

    # singleOrdersInquiry()
    # middleCandle()
    # walletHistory()
    # keyInfo()
    # price = pyupbit.get_current_price("KRW-XRP")
    # conslePrint(price)