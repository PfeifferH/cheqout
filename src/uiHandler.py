import os
import sys
import time
sys.path.append('../cheqout/src')
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from client import Client
import barcode_detect
from barcode_detect import *

from cart_interface import Ui_MainWindow
from cart_interface_produce import Ui_produceWindow
from cart_interface_produce_enter import Ui_ProdEnterWindow
from payment_barcode_interface import Ui_PayWindow

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

layout_index = 0

class ButtonThread(QThread):

    def __init__(self, app):
        super().__init__()
        self.mainWindow = app

    def run(self):
        pre_red = False
        pre_yellow = False
        pre_green = False

        while True:
            if GPIO.input(red) and not pre_red:
                print("red")
                self.mainWindow.red_signal.emit()
                pre_red = True
            elif not GPIO.input(red):
                pre_red = False
            if GPIO.input(yellow) and not pre_yellow:
                print("yellow")
                self.mainWindow.yellow_signal.emit()
                pre_yellow = True
            elif not GPIO.input(yellow):
                pre_yellow = False
            if GPIO.input(green) and not pre_green:
                print("green")
                self.mainWindow.green_signal.emit()
                pre_green = True
            elif not GPIO.input(green):
                pre_green = False

class ScanThread(QThread):

    def __init__(self, app):
        super().__init__()
        self.mainWindow = app

    def run(self):
        while True:
            code = barcode_detect.get_barcode(False)
            self.mainWindow.barcode_signal.emit(code.decode("utf-8"))

def main():

    #initialize application
    app = QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


class ApplicationWindow(QMainWindow):


    # triggers for button presses
    barcode_signal = pyqtSignal(str)
    red_signal = pyqtSignal()
    yellow_signal = pyqtSignal()
    green_signal = pyqtSignal()

    def found_barcode(self, code):
        code = code[1:]
        print(code)
        self.cart.add_item(code)

    def red_click(self):
        if layout_index == 0:
            pass
        elif layout_index == 1:
            pass
        elif layout_index == 2:
            pass
        else:
            pass
        self.scanClick()

    def yellow_click(self):
        if layout_index == 0:
            pass
        elif layout_index == 1:
            pass
        elif layout_index == 2:
            pass
        else:
            pass
        self.produceClick()

    def green_click(self):
        if layout_index == 0:
            pass
        elif layout_index == 1:
            pass
        elif layout_index == 2:
            pass
        else:
            pass
        self.produceEnterClick()


    def produceClick(self):
        layout_index = 1
        self.StackedLayout.setCurrentIndex(1)

    def produceEnterClick(self):
        layout_index = 2
        self.StackedLayout.setCurrentIndex(2)

    def payClick(self):
        layout_index = 3
        self.StackedLayout.setCurrentIndex(3)

    def mainClick(self):
        layout_index = 0
        self.StackedLayout.setCurrentIndex(0)

    def all_done(self):
        self.cart.deactivate()

    def __init__(self):
        # Set up api
        self.cart = Client("../keys/cheqout-57ee7-firebase-adminsdk-8b1oa-8dd14d0e11.json", 'ULtXMhOuqcRHPpa2aKy1')
        self.cart.activate()


        super(ApplicationWindow, self).__init__()
        self.resize(800, 480)
        self.StackedLayout = QStackedLayout()
        # Setup the main window
        layout_index = 0
        MainWindow = QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        self.StackedLayout.addWidget(MainWindow)


        produce = QDialog()
        produceUi = Ui_produceWindow()
        produceUi.setupUi(produce)

        produceEnter = QMainWindow()
        produceEnterUi = Ui_ProdEnterWindow()
        produceEnterUi.setupUi(produceEnter)

        payEnter = QMainWindow()
        payEnterUi = Ui_PayWindow()
        payEnterUi.setupUi(payEnter)

        self.StackedLayout.addWidget(produce)
        self.StackedLayout.addWidget(produceEnter)
        self.StackedLayout.addWidget(payEnter)
        self.MainWidget = QWidget()
        self.MainWidget.setLayout(self.StackedLayout)
        self.setCentralWidget(self.MainWidget)
        self.StackedLayout.setCurrentIndex(0)

        ui.pushButton_2.clicked.connect(self.produceClick)
        ui.pushButton_3.clicked.connect(self.payClick)

        produceUi.pushButton_2.clicked.connect(self.produceEnterClick)

        produceEnterUi.pushButton_2.clicked.connect(self.mainClick)
        produceEnterUi.pushButton_3.clicked.connect(self.mainClick)

        priceTotal = 0
        for i in range(len(self.cart.get_items())):
            priceTotal+= self.cart.get_items()[i]['price']
            cartItem = QListWidgetItem(self.cart.get_items()[i]['name'] + " " + str(self.cart.get_items()[i]['price']))
            ui.listWidget.addItem(cartItem)

        cartItem = QListWidgetItem("TOTAL PRICE: " + str(priceTotal))
        ui.listWidget.addItem(cartItem)




        atexit.register(self.all_done)

        # setup threading signals to work with buttons
        self.red_signal.connect(self.red_click)
        self.yellow_signal.connect(self.yellow_click)
        self.green_signal.connect(self.green_click)
        self.barcode_signal.connect(self.found_barcode)
        self.button_thread = ButtonThread(self)
        self.button_thread.start()
        self.barcode_thread = ScanThread(self)
        self.barcode_thread.start()

if __name__ == "__main__":
    main()
