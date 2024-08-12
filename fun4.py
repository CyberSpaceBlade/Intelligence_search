import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import *
import Formula


class Query(QObject):
    def __init__(self, parent=None):
        super(Query, self).__init__(parent)
        self.ip1 = None
        self.ui = QUiLoader().load('UI/Fun4.ui')
        self.ui.pushButton.clicked.connect(self.pushButton_clicked)

    def pushButton_clicked(self):
        self.ui.lineEdit_3.setText("")
        self.ui.lineEdit_4.setText("")
        self.ui.lineEdit_5.setText("")
        self.ui.lineEdit_6.setText("")
        self.ui.lineEdit_7.setText("")
        self.ui.lineEdit_8.setText("")

        QTimer.singleShot(100, lambda: self.display_result())

    def display_result(self):
        self.ip1 = self.ui.lineEdit_2.text().strip()
        res_list = Formula.ip_loc(self.ip1)
        try:
            self.ui.lineEdit_3.setText(res_list[0])
            self.ui.lineEdit_4.setText(res_list[1])
            self.ui.lineEdit_5.setText(res_list[2])
            self.ui.lineEdit_6.setText(res_list[3])
            self.ui.lineEdit_7.setText(res_list[4])
            self.ui.lineEdit_8.setText(res_list[5])
        except:
            pass


def main():
    q = QUiLoader()
    app = QApplication([])
    q = Query()
    q.ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
