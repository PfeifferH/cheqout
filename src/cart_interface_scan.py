# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cart_interface_scan.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ScanWindow(object):
    def setupUi(self, ScanWindow):
        ScanWindow.setObjectName("ScanWindow")
        ScanWindow.resize(800, 480)
        self.textBrowser = QtWidgets.QTextBrowser(ScanWindow)
        self.textBrowser.setGeometry(QtCore.QRect(0, 120, 400, 160))
        self.textBrowser.setAutoFillBackground(False)
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton_2 = QtWidgets.QPushButton(ScanWindow)
        self.pushButton_2.setGeometry(QtCore.QRect(200, 330, 400, 80))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(ScanWindow)
        QtCore.QMetaObject.connectSlotsByName(ScanWindow)

    def retranslateUi(self, ScanWindow):
        _translate = QtCore.QCoreApplication.translate
        ScanWindow.setWindowTitle(_translate("ScanWindow", "Dialog"))
        self.textBrowser.setHtml(_translate("ScanWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">PLEASE SCAN YOUR ITEM AND PLACE IT IN THE CART</span></p></body></html>"))
        self.pushButton_2.setText(_translate("ScanWindow", "CONTINUE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ScanWindow = QtWidgets.QDialog()
    ui = Ui_ScanWindow()
    ui.setupUi(ScanWindow)
    ScanWindow.show()
    sys.exit(app.exec_())

