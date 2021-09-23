
from PyQt5 import QtCore, QtGui, QtWidgets
from libary import tickerInfo

# Coin
import coin

# Libary
import json

# GUI
from gui import textBox
import sys

global tickerInfoList

class makeFunction(object):
    
    # 생성자
    def __init__(self, ui):
      self.ui = ui
      self.initButtonFunction();
      self.initComboBoxItem()
      return

    # 버튼에 기능 연결
    def initButtonFunction(self):
        self.ui.accountsInquiryBtn.clicked.connect(self.accountsInquiryBtnClick)
        self.ui.singleOrdersInquiry.clicked.connect(self.singleOrdersInquiryBtnClick)
        self.ui.fiatKRW.stateChanged.connect(self.updateComboBoxItem)
        self.ui.fiatBTC.stateChanged.connect(self.updateComboBoxItem)
        self.ui.fiatUSDT.stateChanged.connect(self.updateComboBoxItem)
        return


    # 콤보박스에 데이터 넣기
    def initComboBoxItem(self) :
        self.ui.fiatKRW.setCheckState(2)
        self.updateComboBoxItem()

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

          self.ui.singleOrderItems.addItem(data[0] + "(" + data[2] + ")", data[1]);
      return

    # 텍스트에 표시하기
    def showText(self, requestString):
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.setPlainText(requestString)
        return

    # 전체 계좌조회 버튼 클릭
    # self.accountsInquiryBtn.setObjectName("accountsInquiryBtn")
    def accountsInquiryBtnClick(self):
        jsonStr = coin.accountsInquiry()
        str = json.dumps(jsonStr, indent="\n")
        self.showText("전체 계좌조회\n" + str)
        return



    # 단일 주문조회 버튼 클릭
    # self.singleOrdersInquiry.setObjectName("singleOrdersInquiry")$
    def singleOrdersInquiryBtnClick(self):
        curTicker = self.ui.singleOrderItems.currentData()
        self.showText("단일 주문조회\n" + coin.singleOrdersInquiry(curTicker))
        return


def initTextBoxControl():
    app = QtWidgets.QApplication(sys.argv)
    GroupBox = QtWidgets.QGroupBox()
    ui = textBox.Ui_GroupBox()
    ui.setupUi(GroupBox)
    uiFunction = makeFunction(ui)
    GroupBox.show()
    sys.exit(app.exec_())
    return


if __name__ == '__main__':  # 프로그램의 시작점일 때만 아래 코드 실행
    tickerInfoList = tickerInfo.getTickInfo()
    initTextBoxControl()