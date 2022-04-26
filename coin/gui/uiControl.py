
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import *

from PyQt5.QtWidgets import *
from PyQt5 import uic

from libary import tickerInfo
from libary import excuteFile

from threading import Thread

# Coin
import coin

# Libary
import time
import datetime

# GUI
from gui import ui
import sys

global tickerInfoList

def getMoneyValue(value, flat = "KRW", roundValue = 0):
    fValue = float(value)
    
    if roundValue == 0:
        nValue = round(fValue)
    else:
        nValue = round(fValue, roundValue)

    valueStr = format(nValue, ",") + " " + flat
    return valueStr

class WorkerThread(QThread):
    finished = pyqtSignal() 
    
    def run(self):
        while True:
            self.finished.emit()
            self.sleep(1)
        return

class MainWindow(QMainWindow, QGroupBox):
   
    # 생성자
    def __init__(self, ui):
      super().__init__()

      self.ui = ui;
      self.initSelectCoinInfo();    #  코인정보 세팅

      # Thread
      self.worker = WorkerThread()
      self.worker.finished.connect(self.updateAccountsInquiryInfo)
      self.worker.finished.connect(self.updateCandle) # 이건 뭐지
      self.worker.start()

      return

    # 버튼에 기능 연결
    def initSelectCoinInfo(self):
        self.initSelectCoinInfoComboBoxItem()   # 콤보박스 데이터 넣기 

        # 체크박스의 데이터 넣기
        self.ui.fiatKRW.stateChanged.connect(self.updateComboBoxItem)
        self.ui.fiatBTC.stateChanged.connect(self.updateComboBoxItem)
        self.ui.fiatUSDT.stateChanged.connect(self.updateComboBoxItem)

        # 주문가능정보 테스트
        self.ui.test_buyButton.clicked.connect(self.order)
        return


    # 콤보박스에 데이터 넣기
    def initSelectCoinInfoComboBoxItem(self) :
        self.ui.fiatKRW.setCheckState(2)
        self.updateComboBoxItem()
        
        # 콤보박스와 연결 된 텍스트 업데이트
        self.ui.singleOrderItems.currentIndexChanged.connect(self.updateSelectCoinText)
        return

    # 콤보박스에 데이터 업데이트하기
    def updateComboBoxItem(self) :
        # self.singleOrderItems = QtWidgets.QComboBox(self.verticalLayoutWidget)
      

      hideItemFiter = [['KRW-KRW', False] # 원화는 강제로 제거
                    ,['KRW', self.ui.fiatKRW.isChecked()]
                    ,['BTC', self.ui.fiatBTC.isChecked()]
                    ,['USDT', self.ui.fiatUSDT.isChecked()]]

      self.ui.singleOrderItems.clear()
      for data in tickerInfoList:
          isContinue = False
          for fiter in hideItemFiter:
              if fiter[0] not in data[2]:
                continue
              
              if fiter[1] == False:
                  isContinue = True
                  break;
        
          if isContinue == True:
              continue

          str = data[0] + "(" + data[2] + ")", data[1]
          self.ui.singleOrderItems.addItem(data[0] + "(" + data[2] + ")", data[1]);
      return
    
    # 콤보박스의 데이터 업데이트하기
    def updateSelectCoinText(self):
        markets = self.ui.singleOrderItems.currentData()
        if markets == None:
           return

        response = coin.currentCoinPriceInfo(markets)
        if response.status_code != 200:
            print("coin.currentCoinPriceInfo(markets) ErrorType(" + str(response.status_code) + ") Reason(" + response.reason + ")")
            return

        data = response.json()
        flat = markets.split('-')[0]
        try:
            for info in data:
               text = getMoneyValue(info['trade_price'])

        except Exception as x:
           text = (x.__class__.__name__)

        self.ui.textBrowser_TargetCoinPrice.setPlainText(text)
        return

        
    # 텍스트에 표시하기
    def showText(self, requestString):
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.setPlainText(requestString)
        return

    # 내 계좌정보 업데이트
    @pyqtSlot()
    def updateAccountsInquiryInfo(self):
        accountJsonData = coin.accountsInquiry()

        totalEvaluatedPrice = 0.0
        totalBuyPrice = 0.0
        current_money = 0.0

        for data in accountJsonData:

            currency = data['currency']
            unit_currency = data['unit_currency']
            if currency == 'KRW':
                current_money = data['balance']
                self.ui.textBrowser_current_money.setPlainText(getMoneyValue(current_money))
                continue

            markets = unit_currency + '-' + currency
            
            balance = float(data['balance'])
            response = coin.currentCoinPriceInfo(markets)
             
            totalBuyPrice += balance *  float(data['avg_buy_price']) # 매수 금액 Sum

            if response.status_code == 404:
                continue

            if response.status_code != 200:
                print ("coin.currentCoinPriceInfo(markets) ErrorType(" + str(response.status_code) + ") Reason(" + response.reason + ")")
                continue

            jsonPriceData = response.json()
            for info in jsonPriceData:
                price = float(info['trade_price'])
                totalEvaluatedPrice += balance * price  # 총 평가금액


        self.ui.textBrowser_total_evaluated_price.setPlainText(getMoneyValue(totalEvaluatedPrice))    # 현재 평가 금액
        self.ui.textBrowser_tootal_buy_price.setPlainText(getMoneyValue(totalBuyPrice))               # 현재 구매 금액

        total_valuation = totalEvaluatedPrice - totalBuyPrice
        self.ui.textBrowser_total_valuation.setPlainText(getMoneyValue(total_valuation))             # 현재 이득

        
        total_earning_percent = 0.0
        if totalEvaluatedPrice > 0:
            total_earning_percent = total_valuation / totalEvaluatedPrice * 100
        self.ui.textBrowser_total_earning_percent.setPlainText(getMoneyValue(total_earning_percent, "%", 3))             # 현재 이득

        total_asset = float(current_money) + totalEvaluatedPrice
        self.ui.textBrowser_total_asset.setPlainText(getMoneyValue(total_asset))                      # 현재  토탈 금액
        return

    def updateCandle(self):
        markets = self.ui.singleOrderItems.currentData()
        if markets == None:
           return
        response = coin.requestCandles(markets)

        return

    # 단일 주문조회 버튼 클릭
    # self.singleOrdersInquiry.setObjectName("singleOrdersInquiry")$
    def singleOrdersInquiryBtnClick(self):
        curTicker = self.ui.singleOrderItems.currentData()
        self.showText("단일 주문조회\n" + coin.singleOrdersInquiry(curTicker))
        return


    #  주문하기
    def order(self):
        markets = self.ui.singleOrderItems.currentData()
        if markets == None:
           return

        coin.orderChance(markets)
        coin.order()
        return

    # 주문 가능정보 조회
    def orderChance(self):
        markets = self.ui.singleOrderItems.currentData()
        if markets == None:
           return

        response = coin.orderChance(markets)
        print(response.json())
        return

if __name__ == '__main__':  # 프로그램의 시작점일 때만 아래 코드 실행
    
    excuteFile.preExcute()

    # 데이터 초기화
    tickerInfoList = tickerInfo.getTickInfo()
    
    app = QtWidgets.QApplication(sys.argv)
   
    groupBox = QtWidgets.QGroupBox()
    ui_ = ui.Ui_GroupBox()
    ui_.setupUi(groupBox)
    groupBox.show()

    global mainWindow
    mainWindow = MainWindow(ui_)
    
    global isLoad
    isLoad = 1

    sys.exit(app.exec_())

  