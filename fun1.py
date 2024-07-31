import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import *
import Formula


class Query(QObject):
    def __init__(self, parent=None):
        super(Query, self).__init__(parent)
        self.ui = QUiLoader().load('UI/Fun1.ui')
        self.ui.pushButton.clicked.connect(self.pushButton_clicked)

    def pushButton_clicked(self):
        ip = str(self.ui.lineEdit.text()).strip()
        res = Formula.ip_search(ip)
        self.ui.lineEdit_2.setText(str(res))
        pass


def main():
    q = QUiLoader()
    app = QApplication([])
    q = Query()
    q.ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
