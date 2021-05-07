import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pybithumb import WebSocketManager
import requests
import time

class OverViewWorker(QThread):
    dataSent = pyqtSignal(dict)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        while self.alive:
            r = requests.get("https://api.bithumb.com/public/ticker/BTC_KRW")
            bitcoin = r.json()
            data = bitcoin['data']
            time.sleep(1)
            if data != None:
                self.dataSent.emit(data)

    def close(self):
        self.alive = False


class OverviewWidget(QWidget):
    def __init__(self, parent=None, ticker="BTC", ):
        super().__init__(parent)
        uic.loadUi("resource/overview.ui", self)

        self.ticker = ticker
        self.ovw = OverViewWorker(ticker)
        self.ovw.dataSent.connect(self.fillData)
        self.ovw.start()

    def closeEvent(self, event):
        self.ovw.close()

    def fillData(self, data):
        self.label_1.setText(f"{int(data['closing_price']):,}")
        self.label_4.setText(f"{float(data['units_traded_24H']):.4f} {self.ticker}")
        self.label_6.setText(f"{int(data['max_price']):,}")
        self.label_8.setText(f"{float(data['acc_trade_value_24H'])/100000000:,.1f} 억")
        self.label_10.setText(f"{int(data['min_price']):,}")
        self.label_14.setText(f"{int(data['prev_closing_price']):,}")
        self.label_2.setText(f"{float(data['fluctate_rate_24H']):+.2f}%")
        #self.label_12.setText(f"{volumePower:.2f}%")
        self.__updateStyle()

    def __updateStyle(self):
        if '-' in self.label_2.text():
            self.label_1.setStyleSheet("color:blue;")
            self.label_2.setStyleSheet("background-color:blue;color:white")
        else:
            self.label_1.setStyleSheet("color:red;")
            self.label_2.setStyleSheet("background-color:red;color:white")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ob = OverviewWidget()
    ob.show()
    sys.exit(app.exec_())
