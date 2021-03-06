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

GPIO.setup(red, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(yellow, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(green, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# ------------------------------------------------------------------------


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
            time.sleep(1)

def main():

    #initialize application
    app = QApplication(sys.argv)
    application = ApplicationWindow()
    application.showFullScreen()
    app.exec_()


class ApplicationWindow(QMainWindow):


    # triggers for button presses
    barcode_signal = pyqtSignal(str)
    red_signal = pyqtSignal()
    yellow_signal = pyqtSignal()
    green_signal = pyqtSignal()

    def found_barcode(self, code):
        # If we are not paying then we are just scanning for a normal item
        if not self.paying:
            print('flag1')
            code = code[1:]
            print(code)
            self.cart.add_item(code)
            print('flag2')
            self.update_items()
            print('flag3')
        # If we are paying then we assume the barcode is a payment thing
        else:
            user = None
            # So we should handle a transaction here
            for document in self.cart.users.get():
                if document.to_dict()['loyalty'] == code:
                    user = document.reference.id
            if user is None:
                print("User wasn't found...")
                return
            self.cart.store_transaction(user)
            print("Transaction succeeded")
            self.paying = False
            # reset the cart after payment
            self.cart.clear()
            self.update_items()
            # return to the main layout
            self.mainClick()

    def update_items(self):
        self.ui.listWidget.clear()
        priceTotal = 0
        shopping_cart = self.cart.get_items()
        for i in range(len(shopping_cart)):
            priceTotal += shopping_cart[i]['price'] * shopping_cart[i]['qty']
            cartItem = QListWidgetItem(shopping_cart[i]['name'] + " " + str(shopping_cart[i]['qty']) + " * " + str(shopping_cart[i]['price']))
            self.ui.listWidget.addItem(cartItem)
        cartItem = QListWidgetItem("TOTAL PRICE: " + str(priceTotal))
        self.ui.listWidget.addItem(cartItem)

    def red_click(self):
        if self.layout_index == 0:
            self.mainClick()
        elif self.layout_index == 1:
            self.mainClick()
        elif self.layout_index == 2:
            self.mainClick()
        else:
            self.mainClick()

    def yellow_click(self):
        if self.layout_index == 0:
            self.payClick()
        elif self.layout_index == 1:
            pass
        elif self.layout_index == 2:
            pass
        else:
            pass

    def green_click(self):
        if self.layout_index == 0:
            self.produceClick()
            #print(self.layout_index)
        elif self.layout_index == 1:
            self.produceEnterClick()
            #print(self.layout_index)
        elif self.layout_index == 2:
            self.mainClick()
            #print(self.layout_index)
        else:
            pass


    def produceClick(self):
        self.layout_index = 1
        self.StackedLayout.setCurrentIndex(1)

    def produceEnterClick(self):
        self.layout_index = 2
        self.StackedLayout.setCurrentIndex(2)

    def payClick(self):
        self.layout_index = 3
        self.StackedLayout.setCurrentIndex(3)
        # Then process the cart for a transaction
        self.paying = True

    def mainClick(self):
        self.layout_index = 0
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
        self.layout_index = 0
        MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
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

        self.ui.pushButton_2.clicked.connect(self.produceClick)
        self.ui.pushButton_3.clicked.connect(self.payClick)

        produceUi.pushButton_2.clicked.connect(self.produceEnterClick)

        produceEnterUi.pushButton_2.clicked.connect(self.mainClick)
        produceEnterUi.pushButton_3.clicked.connect(self.mainClick)


        self.update_items()

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

        # initialize member variables
        self.paying = False

if __name__ == "__main__":
    main()
