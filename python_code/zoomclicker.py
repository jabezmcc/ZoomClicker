from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication, QMessageBox
import os, sys, platform, subprocess
from pyautogui import size as pagsize
from pyautogui import moveTo as pagmoveTo
from pyautogui import click as pagclick
import time
import random
# this is rando branch
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = '1'

Ui_MainWindow, QMainWindow = loadUiType('zoomclicker_rando.ui') 
Ui_AboutWindow, QAboutWindow = loadUiType('about.ui')

vers = '0.2.0'

mousetime = 0.5
screenwidth = pagsize().width
screenheight = pagsize().height
midpoint = screenheight/2
leftx = int(screenwidth*0.025)
rightx = int(screenwidth*0.975)

class About(QAboutWindow, Ui_AboutWindow):
    def __init__(self):
        super(About,self).__init__()
        self.setupUi(self)
        self.versionLabel.setText("Version "+vers)
        self.licenseButt.clicked.connect(self.show_license)
        self.OKButt.clicked.connect(self.closeout)
        self.show()
        
    def show_license(self):
        p = platform.system()
        try:
            if p == 'Linux':
                subprocess.run(['xdg-open', 'LICENSE.txt'],check=True)
            elif p== 'Windows':
                os.system('start LICENSE.txt')
            else:
                os.system('open LICENSE.txt')
        except:
             QMessageBox.warning(self,'Error','<font color=\"White\">Unable to open license document')
                
    def closeout(self):
        self.destroy()

class Worker(QObject):
    nscreens = 2
    timedelay = 5
    def run(self):
        dt = max(3,self.randify(self.timedelay))
        #print(dt)
        time.sleep(dt)
        for i in range(50):
            pagmoveTo(rightx,midpoint,duration=mousetime)
            for i in range(self.nscreens-1):
                pagclick()
                dt = max(3,self.randify(self.timedelay))
                #print(dt)
                time.sleep(dt)
            pagmoveTo(leftx,midpoint,duration=mousetime)
            for i in range(self.nscreens-1):
                pagclick()
                dt = max(3,self.randify(self.timedelay))
                #print(dt)
                time.sleep(dt)

    def getvalues(self, a, b):
        self.nscreens = a
        self.timedelay = b
        #print(a, b)
    
    def randify(self, timedelay):
        pct = main.randoSlider.value()
        rnd = random.random()
        return int(timedelay*(1 + pct/100*(2*rnd - 1)))   

class Main(QMainWindow, Ui_MainWindow):
    valueSignal = pyqtSignal(int, int)
    def __init__(self):
        super(Main,self).__init__()
        self.setupUi(self)
        self.runningLabel.setText("")
        self.minsecCombo.setView(QtWidgets.QListView())
#        self.minsecCombo.setStyleSheet("QListView::item {color: black; background-color: white;}")
#        self.minsecCombo.setStyleSheet("QListView::item {height:25px;}")
        self.actionExit.triggered.connect(self.buttClose)
        self.actionHelp.triggered.connect(self.openhelp)
        self.actionAbout_2.triggered.connect(self.openabout)
        self.randoSlider.setValue(50)
        self.randoLabel.setText('Randomness 50%')
        self.randoSlider.sliderReleased.connect(self.sliderchanged)  
        self.quitButt.clicked.connect(self.buttClose)
        self.startButt.clicked.connect(self.startit)
        self.thread = QThread()
        self.worker = Worker()
        self.show()
    
    def openhelp(self):
        p = platform.system()
        try:
            if p == 'Linux':
                subprocess.run(['xdg-open', 'ZoomClickerHelp.pdf'],check=True)
            elif p=='Windows':
                os.system('start ZoomClickerHelp.pdf')
            else:
                os.system('open ZoomClickerHelp.pdf')    
        except:
            QMessageBox.warning(self,'Error','<font color=\"White\">Unable to open help document')
 
    def openabout(self):
        self.aboutwin = About()
            
    def startit(self):
        self.runningLabel.setText('running...')
        nstext = self.numScreens.text()
        if nstext.isdecimal():
            self.numscreens = int(nstext)
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Warning')
            msgBox.setStyleSheet("background-color:rgb(50,50,50)")
            msgBox.setText('<font color=\"White\">Please enter digits only for number of screens.')
            msgBox.exec_()
            return
        if self.numscreens < 2:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Warning')
            msgBox.setStyleSheet("background-color:rgb(50,50,50)")
            msgBox.setText('<font color=\"White\">Please enter at least 2 screens.')
            msgBox.exec_()
            return
        tdtext = self.timeDelay.text()
        if tdtext.isdecimal():
            self.timedelay = int(tdtext)
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Warning')
            msgBox.setStyleSheet("background-color:rgb(50,50,50)")
            msgBox.setText('<font color=\"White\">Please enter digits only for time delay.')
            msgBox.exec_()
            return
        minsec = self.minsecCombo.currentIndex()
        if not minsec:
            self.timedelay = self.timedelay*60
        if self.timedelay <3:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Warning')
            msgBox.setStyleSheet("background-color:rgb(50,50,50)")
            msgBox.setText('<font color=\"White\">A time dalay of less than 3 sec will cause loss of mouse control!')
            msgBox.exec_()           
            return   
        self.runclickerthread()
            
    def runclickerthread(self):
        self.worker.moveToThread(self.thread)
        self.valueSignal.emit(self.numscreens, self.timedelay)
        self.thread.started.connect(self.worker.run)
        self.thread.start()
        
    def sliderchanged(self):
        a = self.randoSlider.value()
        self.randoLabel.setText('Randomness '+str(a)+'%') 
    
    def buttClose(self):
        try:
            self.aboutwin.close()
        except:
            pass
        sys.exit()
    
    def closeEvent(self,event):
        try:
            self.aboutwin.close()
        except:
            pass
        sys.exit()

if __name__=="__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.valueSignal.connect(main.worker.getvalues)
    sys.exit(app.exec())
    
    

        
