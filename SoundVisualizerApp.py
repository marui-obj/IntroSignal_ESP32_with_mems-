# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myApp.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from pyqtgraph import PlotWidget
from pyqtgraph import mkColor, mkPen
import serial
import numpy as np
import sys
import time
from scipy.io.wavfile import write
from scipy.fft import fft


ser = serial.Serial("COM3", baudrate = 115200, timeout = 1)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 700)
        MainWindow.setStyleSheet("background-color: rgb(39, 39, 39);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 600, 251, 61))
        self.pushButton.setStyleSheet("background-color: rgb(237, 234, 240);border-radius:20px\n""")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda:self.waveSel())

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(520, 600, 251, 61))
        self.pushButton_2.setStyleSheet("background-color: rgb(237, 234, 240);border-radius:20px\n""")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda:self.fftSel())

        self.graphicsView = PlotWidget(self.centralwidget,background=mkColor(80,80,80))
        self.graphicsView.setGeometry(QtCore.QRect(40, 20, 831, 541))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setYRange(-1.5,1.5)
        self.graphicsView.setMouseEnabled(False,False)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 570, 831, 171))
        self.label.setStyleSheet("border-radius:20px;background-color: rgb(65, 64, 65);")
        self.label.setObjectName("label")
        self.graphicsView.raise_()
        self.label.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.h2 = self.graphicsView.plot(pen=mkPen('w',width=2))
        #========================================

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.printInterval)
        self.timer.start()

        #========================================

        ser.flushInput()
        ser.flushOutput()

        #### Set Data  #####################

        self.size = 500
        self.fft = False

        self.x = np.linspace(0,self.size, self.size)
        self.X,self.Y = np.meshgrid(self.x,self.x)

        self.rawData = []
        for k in range(100) : 
            self.rawData.append(0.0)

        #### Start  #####################
        self._update()

    def _update(self):
        # self.data = np.sin(self.X/3.+self.counter/9.)
        # self.ydata = np.array([1,2,3,4,5,6,7])

        while(len(self.rawData)>self.size) : 
            temp = self.rawData
            del self.rawData
            self.rawData = []
            for k in range(len(self.rawData)-self.size,len(self.rawData)) :
                self.rawData.append(temp[k]) 
            del temp

        
        if len(self.rawData)==self.size : 
            self.graphicsView.plot(pen=mkPen('w',width=2))
            yf=self.rawData
            if (self.fft==True) :
                yf = fft(self.rawData)
                yf = np.abs(yf[0:int(self.size / 2)]) * 2 / 20
                self.x=np.linspace(0,10,int(self.size/2))
            self.h2.setData(self.x, yf)
           
        self.label.setText("")
        QtCore.QTimer.singleShot(1, self._update)

        self.data = []
        start = time.time()
        try:
            self.data = ser.read(512).decode("utf-8").split("\r\n")

        except:
            print("Error")
        for k in range(1,len(self.data)-1) :
            try :
                self.rawData.append(float(self.data[k]))
            except :
                print(self.data[k])
        stop = time.time()

       
        if ser.inWaiting()>= 400:
            self.graphicsView = PlotWidget(self.centralwidget,background=mkColor(80,80,80))
            self.graphicsView.setGeometry(QtCore.QRect(40, 20, 731, 441))
            self.graphicsView.setObjectName("graphicsView")
            self.graphicsView.setMouseEnabled(True,True)    
            ser.flushInput()
            ser.flushOutput()
            ser.flush()
            print("reset")
            
           
      
        

    def printInterval(self):
        if self.data:
            #print("done", ser.in_waiting,max(self.data),len(self.data))
            pass
         
            


        
       

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "WAVEFORM"))
        self.pushButton_2.setText(_translate("MainWindow", "FFT"))
        self.label.setText(_translate("MainWindow", "TextLabel"))

    def waveSel(self) :
        self.graphicsView.setYRange(-1.3,1.3)
        self.graphicsView.setXRange(0.9,495)
        self.size = 500
        self.x = np.linspace(0,self.size, self.size)
        self.fft = False
      

    def fftSel(self) :
        self.graphicsView.setXRange(1,10)
        self.graphicsView.setYRange(0,3)
        self.fft = True
        self.size = 100
       
        
        

if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
    