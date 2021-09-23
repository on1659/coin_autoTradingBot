import requests 
import json
import pyupbit

def checkFilter(ticker, fiatList):
        for fiat in fiatList:
            if fiat == "ALL-":
                return True

            if ticker.startswith(fiat):
                return True
        return False

def getKeyPriority(key):
    if key.startswith("KRW"):
        return 0
    if key.startswith("BTC"):
        return 1
    if key.startswith("USTD"):
        return 2
    return 3

def getTickInfo(fiatList = ["ALL-",]):

    tickList = [["KRW-KRW","원화","KRW-KRW"],] 

    try:
        url = "https://api.upbit.com/v1/market/all" 
        resp = requests.get(url) 
        data = resp.json() 

        for coin in data:
            ticker = coin['market']
            korean_name = coin['korean_name']

            if checkFilter(ticker, fiatList) == False:
                continue
            
            coinType = ticker[0:3]
            if ticker[0:4] == 'USDT':
                coinType = ticker[0:4]    
            tickList.append([korean_name, ticker, coinType])
       
        tickList = sorted(tickList, key = lambda x: getKeyPriority(x[2]))
        return tickList
           # tickInfo = korean_name + "(" + ticker[4:] + ")")

    except Exception as x:
        print(x.__class__.__name__)
        return None

if __name__ == '__main__':  # 프로그램의 시작점일 때만 아래 코드 실행
   ticker = getTickInfo()
   print(ticker)