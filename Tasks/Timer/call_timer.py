import datetime
from timer import Ui_Dialog
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox



import sys
class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.run_watch)
        self.timer.setInterval(1000)
        self.mscounter = 0
        self.isreset = True
        self.ui.pushButtonStart.clicked.connect(self.start_watch)
        self.ui.lineEdit.returnPressed.connect(self.start_watch)
        self.ui.pushButtonPause.clicked.connect(self.watch_pause)
        self.ui.pushButtonReset.clicked.connect(self.watch_reset)
        self.showLCD()
    def showLCD(self):
        text = str(datetime.timedelta(seconds=self.mscounter))
        self.ui.lcdNumber.setDigitCount(8)
        if not self.isreset:
            self.ui.lcdNumber.display(text)
        else:
            self.ui.lcdNumber.display('0:00:00')
    def run_watch(self):
        if self.mscounter == 0:
            self.isreset = True
            self.ui.pushButtonReset.setDisabled(True)
            self.ui.pushButtonStart.setDisabled(False)
            self.ui.pushButtonPause.setDisabled(True)
        else :  self.mscounter -= 1
        self.showLCD()
    def start_watch(self):
        if self.mscounter == 0:
                        if int(self.ui.lineEdit.text())<36001 and int(self.ui.lineEdit.text()):
                                
                                self.mscounter = int(self.ui.lineEdit.text())
                                self.ui.lineEdit.clear()
                        else:
                                msg = QMessageBox()
                                msg.setWindowTitle("Alert")
                                msg.setText("Please Enter a time within the range (1:36000)")
                                msg.setIcon(QMessageBox.Critical)
                                x = msg.exec_()  # this will show our messagebox
        else: print("lol")




        self.timer.start()
        self.isreset = False
        self.ui.pushButtonReset.setDisabled(False)
        self.ui.pushButtonStart.setDisabled(True)
        self.ui.pushButtonPause.setDisabled(False)
    def watch_pause(self):
        self.timer.stop()
        self.ui.pushButtonReset.setDisabled(False)
        self.ui.pushButtonStart.setDisabled(False)
        self.ui.pushButtonPause.setDisabled(True)
    def watch_reset(self):
        self.timer.stop()
        self.mscounter = 0
        self.isreset = True
        self.showLCD()
        self.ui.pushButtonReset.setDisabled(True)
        self.ui.pushButtonStart.setDisabled(False)
        self.ui.pushButtonPause.setDisabled(True)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
