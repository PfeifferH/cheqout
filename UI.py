import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'cheqout gui'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 480

        self.initUI()



    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


        self.logo = QLabel("<h1>COMPANY LOGO</h1>", self)
        self.logo.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red; font-size: 48px}')
        self.logo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.logo.resize(300, 50)
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.move(self.width / 2 - 150, 50)

        btnWidth = 500
        btnHeight = 70


        scanBtn = QPushButton('SCAN ITEMS', self)
        scanBtn.setStyleSheet('QPushButton {background-color: #C0C0C0; color: black; font-size: 48px; border-radius: 7px}')
        scanBtn.setToolTip('This is an example button')
        scanBtn.move(self.width / 2 - (btnWidth / 2), 150)
        scanBtn.resize(btnWidth, btnHeight)
        scanBtn.clicked.connect(self.on_click)

        produceBtn = QPushButton('ADD PRODUCE', self)
        produceBtn.setStyleSheet('QPushButton {background-color: #C0C0C0; color: black; font-size: 48px; border-radius: 7px}')
        produceBtn.setToolTip('This is an example button')
        produceBtn.move(self.width / 2 - (btnWidth / 2), 250)
        produceBtn.resize(btnWidth, btnHeight)
        produceBtn.clicked.connect(self.on_click)

        viewItems = QPushButton('ADD PRODUCE', self)
        viewItems.setStyleSheet('QPushButton {background-color: #C0C0C0; color: black; font-size: 48px; border-radius: 7px}')
        viewItems.setToolTip('This is an example button')
        viewItems.move(self.width / 2 - (btnWidth / 2), 350)
        viewItems.resize(btnWidth, btnHeight)
        viewItems.clicked.connect(self.on_click)

        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())