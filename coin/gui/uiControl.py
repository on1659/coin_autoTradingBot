
from PyQt5 import QtCore, QtGui, QtWidgets
from libary import tickerInfo
from threading import Thread

# Coin
import coin

# Libary
import time

# GUI
from gui import ui
import sys

global tickerInfoList

class makeFunction(object):
   
    # 생성자
    def __init__(self, ui):
      self.ui = ui
      self.initSelectCoinInfo();    #  코인정보 세팅
      return

    # 버튼에 기능 연결
    def initSelectCoinInfo(self):
        self.initSelectCoinInfoComboBoxItem()   # 콤보박스 데이터 넣기 

        # 체크박스의 데이터 넣기
        self.ui.fiatKRW.stateChanged.connect(self.updateComboBoxItem)
        self.ui.fiatBTC.stateChanged.connect(self.updateComboBoxItem)
        self.ui.fiatUSDT.stateChanged.connect(self.updateComboBoxItem)
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

        data = coin.currentCoinPriceInfo(markets).json()
        flat = markets.split('-')[0]
        try:
            for info in data:
               price = format(info['trade_price'], ",")
               text = str(price) + " " + flat

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
    def updateAccountsInquiryInfo(self):
        jsonData = coin.accountsInquiry()

        totalPrice = 0.0
        for data in jsonData:

            currency = data['currency']
            unit_currency = data['unit_currency']
            if currency == 'KRW':
                balance = data['balance']
                self.ui.textBox_current_money = balance
                continue

            markets = unit_currency + '-' + currency
            
            balance = float(data['balance'])
            respone = coin.currentCoinPriceInfo(markets)

            if respone.status_code == 404:
                continue

            jsonPriceData = respone.json()
            for info in jsonPriceData:
                price = float(info['trade_price'])
                totalPrice += balance * price

        self.ui.textBox_tootal_buy_price = str(totalPrice)
        return



    # 단일 주문조회 버튼 클릭
    # self.singleOrdersInquiry.setObjectName("singleOrdersInquiry")$
    def singleOrdersInquiryBtnClick(self):
        curTicker = self.ui.singleOrderItems.currentData()
        self.showText("단일 주문조회\n" + coin.singleOrdersInquiry(curTicker))
        return


def runTextBoxGui():
    app = QtWidgets.QApplication(sys.argv)
    GroupBox = QtWidgets.QGroupBox()
    
    global uiFunction
    mainUi = ui.Ui_GroupBox()
    mainUi.setupUi(GroupBox)
    uiFunction = makeFunction(mainUi)
    
    global isLoad
    isLoad = 1
    GroupBox.show()
    sys.exit(app.exec_())
    return


def updateInfo():

    global isLoad
    isLoad = 0

    while (1):
        if isLoad == 0:
            continue
        uiFunction.updateAccountsInquiryInfo()
        #uiFunction.updateSelectCoinText()
        time.sleep(1)

    return



if __name__ == '__main__':  # 프로그램의 시작점일 때만 아래 코드 실행
    
    # 데이터 초기화
    tickerInfoList = tickerInfo.getTickInfo()
    
    # thread 준비
    logicThread = Thread(target = updateInfo)
    logicThread.start()

    # gui run
    runTextBoxGui()

    # thread kill
    logicThread.join()
