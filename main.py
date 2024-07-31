import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader

import fun1
import fun2
import fun3

class Mainwindow:
    def __init__(self):
        self.ui = QUiLoader().load('UI/mainwindow.ui')

        self.ui.pushButton.clicked.connect(self.pushButton_clicked)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_clicked)

    def pushButton_clicked(self):
        self.fun1 = fun1.Query()
        self.fun1.ui.show()

    def pushButton_2_clicked(self):
        self.fun2 = fun2.Query()
        self.fun2.ui.show()

    def pushButton_3_clicked(self):
        self.fun3 = fun3.Query()
        self.fun3.ui.show()


def main():
    loader=QUiLoader()
    app = QApplication(sys.argv)
    mainwindow = Mainwindow()
    mainwindow.ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
