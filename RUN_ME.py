from MainModel import Ui_MainWindow
from Tasks.Timer.call_timer import MyForm
from Tasks.HandTracking import handDetector
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from Tasks.StitchingObjectDetection.SOD_Controller import mywin
import cv2
import numpy as np
import serial

try:
    arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)
except Exception as e:
    pass
    
    
class mywin2(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.me = Ui_MainWindow()
        self.me.setupUi(self)
        self.sodwin = mywin()
        self.timwin = MyForm()
        self.cap = cv2.VideoCapture(0)
        self.detector = handDetector()
        self.scCnt = 0
        self.on = False

    def modify(self,index,newstring):
        return self.task[:index]+newstring+self.task[index+1:]

    def displayImage(self,img,label):
        qformat=QImage.Format_Indexed8
        if len(img.shape)==3:
            if img.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888

        outImage=QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)
        
        outImage=outImage.rgbSwapped()

        outImage = outImage.mirrored(0,0)

        label.setPixmap(QPixmap.fromImage(outImage))
        label.setScaledContents(True)


    def mapping(self):
        x = 249
        y = 499
        fx = 249
        fy = 499
        flag = 0
        lx = 249
        ly = 499
        firstonly = 0
        flags=0
        flagm=0
        pts = [[fx, fy]]
        last = 1
        countNone = 0
        self.task="0000"
        while True:
            self.modify(2,"0")
            canvas = np.zeros((500, 500, 3), dtype = "uint8")
            key = cv2.waitKeyEx(1)
            if(key==-1):
                try:
                    arduino.write('1'.encode())
                except Exception as E:
                    pass
            if (key==108):
                flags=0
                self.modify(0, "x")
            elif (key==109):
                flags=1
                self.modify(0, "y")
            else :
                flags=2
                self.modify(0, "z")            
            if (key==100):
                flagm=0
                self.modify(1, "m")
            else:
                flagm=1
                self.modify(1, "b")
            #arduinoData=flagm
            if(key == 2490368):
                y = y-2
                self.me.direct_2.setText("Up")
                self.modify( 2, "u")
                if(flag != 0):
                    flag = 0
                    fx = x
                    fy = y
                    if(firstonly == 0):
                        firstonly = 1
                        lx = x
                        ly = y+2
                    pts.insert(last, [fx, fy])
                    last = last + 1
                countNone = 0
            elif (key == 2621440):
                y = y+2
                self.me.direct_2.setText("Down")
                self.modify(2, "d")
                if(flag != 1):
                    flag = 1
                    fx = x
                    fy = y
                    if(firstonly == 0):
                        firstonly = 1
                        lx = x
                        ly = y-2
                    pts.insert(last, [fx, fy])
                    last = last + 1
                countNone = 0
            elif (key == 2424832):
                x = x-2
                self.modify( 2, "l")
                self.me.direct_2.setText("Left")

                if(flag != 2):
                    flag = 2
                    fx = x
                    fy = y
                    if(firstonly == 0):
                        firstonly = 1
                        lx = x+2
                        ly = y
                    pts.insert(last, [fx, fy])
                    last = last + 1
                countNone = 0
            elif (key == 2555904):
                x = x+2
                self.modify( 2, "r")
                self.me.direct_2.setText("Right")

                if(flag != 3):
                    flag = 3
                    fx = x
                    fy = y
                    if(firstonly == 0):
                        firstonly = 1
                        lx = x-2
                        ly = y
                    pts.insert(last, [fx, fy])
                    last = last + 1
                countNone = 0
            else:
                countNone += 1
                if countNone>20:
                    self.me.direct_2.setText("None")

                
            if(firstonly == 0):
                cv2.line(canvas, (249, 499), (x, y), (0, 0, 255), 2)
            elif(firstonly == 1):
                cv2.line(canvas, (249, 499), (lx, ly), (0, 0, 255), 2)
            pts[last - 1][0] = x
            pts[last - 1][1] = y

            arr = np.array(pts)
            arr = arr.reshape((-1, 1, 2))
            cv2.polylines(canvas, [arr], False, (0, 0, 255), 2)
            #cv2.imshow("",canvas)
            #cv2.imwrite("canvas.jpg",canvas)
            self.displayImage(canvas,self.me.mapping)
            success, self.img = self.cap.read()
            self.img = self.detector.findHands(self.img,True)
            lmList = self.detector.findPosition(self.img)
            if len(lmList) != 0:                        #if it detects hand
                totalFingers = self.detector.fingerCounter(lmList)
                if totalFingers>0:
                    print(totalFingers)
                    self.modify(3,str(totalFingers))
            try:
                arduinoData = bytes(self.task, 'ascii')
                arduino.write(arduinoData)
                self.USBconnected()
            except Exception as e:
                self.USBdisconnected()
            self.displayImage(self.img,self.me.camera)
            cv2.waitKey(1)
            self.me.sod.clicked.connect(self.doSod)
            self.me.timer.clicked.connect(self.doTimer)
            self.me.sc.clicked.connect(self.setClicked)
            if self.on:
                self.scs()
            try:
                data = arduino.readline()
                data = data.decode('utf-8')
                if data == "Yes" or data == "No":
                    self.me.leakage.setText(data)
                elif data[0]=="v":
                    self.me.volt.setText(data[1:]+"V")
                elif data[0]=="c":
                    self.me.current.setText(data[1:]+"A")
                self.USBconnected()
            except Exception as e:
                self.USBdisconnected()
                


    def setClicked(self):
        self.on = True
            

    def scs(self):
        self.on = False
        self.scCnt += 1
        cv2.imshow("Screenshot " + str(self.scCnt),self.img)
        cv2.imwrite("Screenshots\Screenshot " + str(self.scCnt) + ".jpg",self.img)
        
        
        
 
    def doSod(self):
        self.sodwin.show()

    def doTimer(self):
        self.timwin.show()

    def USBconnected(self):
        self.me.label.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.me.USB.setText("USB CONNECTED")

    def USBdisconnected(self):
        self.me.label.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.me.USB.setText("Connect USB")
        self.me.volt.setText("0V")
        self.me.current.setText("0A")
        self.me.leakage.setText("No")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    me = mywin2()
    me.show()
    me.mapping()
    sys.exit(app.exec_())



    
