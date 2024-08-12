import sys

from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import *
import Formula


def Xlsx_File_suffix_check(file_path):
    excel_name = file_path.split("/")[-1]
    suffix = str(excel_name).split(".")[-1]
    if suffix != "xlsx":
        res = "请选择xlsx格式的情报表!"
    else:
        res = excel_name
    return res


class Query(QObject):
    def __init__(self, parent=None):
        super(Query, self).__init__(parent)
        self.name1 = None
        self.ui = QUiLoader().load('UI/Fun1.ui')
        self.ui.pushButton.clicked.connect(self.pushButton_clicked)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_clicked)

    def pushButton_clicked(self):
        self.ui.lineEdit_2.setText("")
        if self.name1 is None:
            try:
                self.name1 = 'Inte-All.xlsx'
                self.ui.lineEdit_3.setText("默认")
            except:
                self.ui.lineEdit_3.setText("未指定情报表!")

        QTimer.singleShot(100, lambda: self.display_result())

    def display_result(self):
        ip = str(self.ui.lineEdit.text()).strip()
        res = Formula.ip_search(ip, self.name1)
        self.ui.lineEdit_2.setText(str(res))
        pass

    def pushButton_2_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(QMainWindow(), "选择情报表")
        res = Xlsx_File_suffix_check(file_path)
        self.ui.lineEdit_3.setText(res)
        self.name1 = file_path


def main():
    q = QUiLoader()
    app = QApplication([])
    q = Query()
    q.ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
