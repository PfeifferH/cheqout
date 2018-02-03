import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ../src/client.py import *

from cart_interface import Ui_MainWindow
from cart_interface_scan import Ui_ScanWindow
from cart_interface_produce import Ui_produceWindow
from cart_interface_items import Ui_ItemWindow


def main():

    client.init

    app = QApplication(sys.argv)

    application = ApplicationWindow()
    application.show()
    # sys.exit(app.exec_())
    app.exec_()


class ApplicationWindow(QMainWindow):
    def scanClick(self):
        self.StackedLayout.setCurrentIndex(1)


    def produceClick(self):
        self.StackedLayout.setCurrentIndex(2)


    def itemsClick(self):
        self.StackedLayout.setCurrentIndex(3)


    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.resize(640, 480)
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


if __name__ == "__main__":
    main()