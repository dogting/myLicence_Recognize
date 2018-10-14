# !/user/bin/env python
# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import *
import sys,os
from carGUI import Ui_MainWindow
import video_track
import urllib.request

class MyVideoForm(QMainWindow,Ui_MainWindow):
    # 为了实时显示代码，定义显示信号
    Signal_Log = QtCore.pyqtSignal(str)
    global timesflag
    timesflag = 0

    def __init__(self, parent=None):
        super(MyVideoForm, self).__init__(parent)
        self.setupUi(self)



        self.pushButton.clicked.connect(lambda:self.videoHandle(self.fileLineEdit.text()))     #开始视频处理
        self.fileButton.clicked.connect(lambda:self.openfile(self.fileLineEdit.text()))     #打开文件
        self.SearchButton.clicked.connect(lambda:self.carFind(self.carLicenseLineEdit.text()))  #检索车牌号
        self.mapShow.clicked.connect(lambda:self.maptoshow())
        self.carPic.clicked.connect(lambda:self.pictoshow())

        self.vbox = QtWidgets.QVBoxLayout()
        self.Signal_Log.connect(self.log)


    def carFind(self,carLiscence):
        import SQL_Store
        SQL_Store.SQL_store.searchLiscence(self,'car',carLiscence)

        #开始视频处理，引入video_track
    def videoHandle(self,filePath):
        r = os.path.exists(filePath)
        if r is False:
            print("no file...")
        else:
            pathDir = os.listdir(filePath)
            for allDir in pathDir:
                child = filePath+'/'+allDir
                cameraID = allDir
                video_track.video_track(self,child).get_video(cameraID)


    def openfile(self, filePath):

        if os.path.exists(filePath):
                    path = QFileDialog.getExistingDirectory(self,"Open File Dialog","./")
                    # path = QFileDialog.getOpenFile(self,"Open File Dialog",filePath,"All file(*.*)")
        else:
                    path = QFileDialog.getExistingDirectory(self,"Open File Dialog","./")

        self.fileLineEdit.setText(str(path))

    def maptoshow(self):
        self.log(string="x&show",flag=1)
    def pictoshow(self):
        self.log(string="x&show",flag=0)
    #定义显示的槽函数
    def log(self,string="",image="",flag = 0):
        strlist = str(string).split('&')
        global  timesflag
        if flag ==1 and len(strlist)>1:
            if timesflag !=1:
                timesflag =1
                if not self.gridLayout.isEmpty():
                    self.vbox.removeWidget(self.label_4)
                    self.gridLayout.removeItem(self.vbox)
                self.webview = QWebEngineView()
                path = os.getcwd().split('\\')
                source=""
                for i in path:
                    source +=i+'/'
                print('file:///'+source+'test.html')
                self.webview.load(
                    QtCore.QUrl('file:///'+source+'test.html'))
                self.vbox.addWidget(self.webview)
                self.gridLayout.addLayout(self.vbox, 0, 0)
        # just show
        elif len(strlist)>1:
            # pic show
            if not self.gridLayout.isEmpty() and timesflag !=3:
                self.gridLayout.removeItem(self.vbox)
                self.vbox.removeWidget(self.webview)
            if timesflag == 3:
                self.vbox.removeWidget(self.label_4)

            timesflag = 3
            self.image = QtGui.QImage(os.getcwd() + '/a.jpg')
            self.label_4 = QtWidgets.QLabel(self.centralwidget)
            self.label_4.setPixmap(QtGui.QPixmap.fromImage(self.image))
                # vbox = QtWidgets.QVBoxLayout()
            self.vbox.addWidget(self.label_4)
            self.gridLayout.addLayout(self.vbox, 0, 0)
            # sql show
            if strlist[0] != 'x':
                stritem = strlist[0].split(';')
                string = ""

                for i in range(len(stritem)-2):
                    string += stritem[i]+"\r\n"
                self.resultShowText.setText(str(string))
        else:
            self.resultShowText.setText(str(string))
        cursor = self.resultShowText.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.resultShowText.setTextCursor(cursor)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = MyVideoForm()
    form.show()
    sys.exit(app.exec_())