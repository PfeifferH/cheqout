import os
import sys
sys.path.append('../cheqout/src')
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from client import *

from cart_interface import Ui_MainWindow
from cart_interface_scan import Ui_ScanWindow
from cart_interface_produce import Ui_produceWindow
from cart_interface_items import Ui_ItemWindow

import atexit

def main():

    #initialize application
    app = QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


class ApplicationWindow(QMainWindow):
    def scanClick(self):
        add_item(self.cart, "WAFERS")
        self.StackedLayout.setCurrentIndex(1)

    def produceClick(self):
        self.StackedLayout.setCurrentIndex(2)
        add_item(self.cart, "ONIONS")

    def itemsClick(self):
        self.StackedLayout.setCurrentIndex(3)

    def mainClick(self):
        self.StackedLayout.setCurrentIndex(0)

    def all_done(self):
        deactivate(self.cart)

    def __init__(self):
        # Set up api
        self.cart = init("keys/cheqout-57ee7-firebase-adminsdk-8b1oa-8dd14d0e11.json", 'ULtXMhOuqcRHPpa2aKy1')
        activate(self.cart)


        super(ApplicationWindow, self).__init__()
        self.resize(800, 480)
        self.StackedLayout = QStackedLayout()
        # Setup the main window
        MainWindow = QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        self.StackedLayout.addWidget(MainWindow)
        # Setup the second window
        scans = QDialog()
        scansUi = Ui_ScanWindow()
        scansUi.setupUi(scans)

        produce = QDialog()
        produceUi = Ui_produceWindow()
        produceUi.setupUi(produce)

        items = QMainWindow()
        itemUi = Ui_ItemWindow()
        itemUi.setupUi(items)

        self.StackedLayout.addWidget(scans)
        self.StackedLayout.addWidget(produce)
        self.StackedLayout.addWidget(items)
        self.MainWidget = QWidget()
        self.MainWidget.setLayout(self.StackedLayout)
        self.setCentralWidget(self.MainWidget)
        self.StackedLayout.setCurrentIndex(0)

        ui.pushButton.clicked.connect(self.scanClick)
        ui.pushButton_2.clicked.connect(self.produceClick)
        ui.pushButton_3.clicked.connect(self.itemsClick)

        scansUi.pushButton_2.clicked.connect(self.mainClick)

        produceUi.pushButton_2.clicked.connect(self.mainClick)

        itemUi.pushButton_2.clicked.connect(self.mainClick)


        atexit.register(self.all_done)

if __name__ == "__main__":
    main()