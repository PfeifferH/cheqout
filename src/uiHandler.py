import os
import sys
sys.path.append('../cheqout/src')
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from client import Client
#from barcode_detect import *

from cart_interface import Ui_MainWindow
from cart_interface_scan import Ui_ScanWindow
from cart_interface_produce import Ui_produceWindow
from cart_interface_produce_enter import Ui_ProdEnterWindow

import atexit

# ------------------------ BUTTON PRESS CONSTANTS -----------------------
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

red = 23
yellow = 24
green = 25

GPIO.setup(red, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(yellow, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(green, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# ------------------------------------------------------------------------

red_func = lambda: None
yellow_func = lambda: None
green_func = lambda: None

class ButtonThread(QThread):

    def run(self):
        pre_red = False
        pre_yellow = False
        pre_green = False

        while True:
            if GPIO.input(red) and not pre_red:
                print("red")
                red_func()
                pre_red = True
            else:
                pre_red = False
            if GPIO.input(yellow) and not pre_yellow:
                print("yellow")
                yellow_func()
                pre_yellow = True
            else:
                pre_yellow = False
            if GPIO.input(green) and not pre_green:
                print("green")
                green_func()
                pre_green = True
            else:
                pre_green = False



def main():

    #initialize application
    app = QApplication(sys.argv)
    thread = ButtonThread()
    thread.finished.connect(app.exit)
    application = ApplicationWindow()
    application.show()
    red_func = application.scanClick()
    yellow_func = application.produceClick()
    green_func = application.produceEnterClick()
    thread.start()
    app.exec_()


class ApplicationWindow(QMainWindow):
    def scanClick(self):
        # newItem = get_barcode(self)
        # add_item(self.cart, newItem)
        Client.add_item(self.cart, 'Tri-team-members')
        self.StackedLayout.setCurrentIndex(1)

    def produceClick(self):
        self.StackedLayout.setCurrentIndex(2)

    def produceEnterClick(self):
        self.StackedLayout.setCurrentIndex(3)


    def mainClick(self):
        self.StackedLayout.setCurrentIndex(0)

    def all_done(self):
        Client.deactivate(self.cart)

    def __init__(self):
        # Set up api
        self.cart = Client("keys/cheqout-57ee7-firebase-adminsdk-8b1oa-8dd14d0e11.json", 'ULtXMhOuqcRHPpa2aKy1')
        Client.activate(self.cart)


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

        produceEnter = QMainWindow()
        produceEnterUi = Ui_ProdEnterWindow()
        produceEnterUi.setupUi(produceEnter)

        self.StackedLayout.addWidget(scans)
        self.StackedLayout.addWidget(produce)
        self.StackedLayout.addWidget(produceEnter)
        self.MainWidget = QWidget()
        self.MainWidget.setLayout(self.StackedLayout)
        self.setCentralWidget(self.MainWidget)
        self.StackedLayout.setCurrentIndex(0)

        ui.pushButton.clicked.connect(self.scanClick)
        ui.pushButton_2.clicked.connect(self.produceClick)
        #ui.pushButton_3.clicked.connect(self.itemsClick)

        scansUi.pushButton_2.clicked.connect(self.mainClick)

        produceUi.pushButton_2.clicked.connect(self.produceEnterClick)

        produceEnterUi.pushButton_2.clicked.connect(self.mainClick)
        produceEnterUi.pushButton_3.clicked.connect(self.mainClick
                                                    )
        priceTotal = 0
        for i in range(len(Client.get_items(self.cart))):
            priceTotal+= Client.get_items(self.cart)[i]['price']
            cartItem = QListWidgetItem(Client.get_items(self.cart)[i]['name'] + " " + str(Client.get_items(self.cart)[i]['price']))
            ui.listWidget.addItem(cartItem)

        cartItem = QListWidgetItem("TOTAL PRICE: " + str(priceTotal))
        ui.listWidget.addItem(cartItem)




        atexit.register(self.all_done)

if __name__ == "__main__":
    main()
