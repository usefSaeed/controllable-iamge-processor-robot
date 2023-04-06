from SOD_Model import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage, QPixmap

import cv2 
from StitchingLogic import Stitcher
from objDet2 import objDet

class mywin(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        
        self.me = Ui_MainWindow()
        self.me.setupUi(self)
        self.imgarr = []
        self.me.browse.clicked.connect(self.search)
        self.me.enter.clicked.connect(self.execute)
        
        self.b1 = self.b2 = self.b3 = self.b4 = self.b5 = False

        self.me.enter.setDisabled(True)


    def search(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file', 'D:',  'Images (*.png, *.xmp *.jpg)')
        self.me.path.setText(fname[0])
        img = cv2.imread(fname[0],1)
        img = cv2.resize(img, (350,500))
        #cv2.imshow("img",img)
        pixmap = QtGui.QPixmap(fname[0])
        pixmap_resized = pixmap.scaled(300, 250, QtCore.Qt.IgnoreAspectRatio)
        if not self.b1:
            self.b1 = True
            self.me.im1.setPixmap(pixmap_resized)
            self.imgarr.insert(0,img)
        elif not self.b2:
            self.b2 = True
            self.imgarr.insert(1,img)
            self.me.im2.setPixmap(pixmap_resized)
        elif not self.b3:
            self.b3 = True
            self.imgarr.insert(2,img)
            self.me.im3.setPixmap(pixmap_resized)
        elif not self.b4:
            self.b4 = True
            self.imgarr.insert(3,img)
            self.me.im4.setPixmap(pixmap_resized)
        elif not self.b5:
            self.b5 = True
            self.imgarr.insert(4,img)
            self.me.im5.setPixmap(pixmap_resized)
            self.me.enter.setDisabled(False)

    def execute(self):
        stitch = Stitcher()
        stitch.imgarr = self.imgarr
        stitch.join()
        image = stitch.maxWidth()
        cv2.imwrite("SOD Outputs\Output.jpg",image)
        obj = objDet()
        self.display(obj.img,self.me.output)
    def display(self,im,label):
        qformat=QImage.Format_Indexed8
        if len(im.shape)==3:
            if im.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
        outImage=QImage(im,im.shape[1],im.shape[0],im.strides[0],qformat)
        outImage=outImage.rgbSwapped()
        label.setPixmap(QPixmap.fromImage(outImage))
        label.setScaledContents(True)
        


           
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    me = mywin()
    me.show()
    sys.exit(app.exec_())


    
