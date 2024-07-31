import sys

from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import *
import Formula


def Xlsx_File_suffix_check(file_path):
    if file_path == "":
        res = "请选择合适的情报表!"
    else:
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
        self.name1 = self.name2 = self.name3 = None

        self.ui = QUiLoader().load('UI/Fun2.ui')
        self.ui.pushButton.clicked.connect(self.pushButton_clicked)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_clicked)
        self.ui.pushButton_4.clicked.connect(self.pushButton_4_clicked)

    def pushButton_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(QMainWindow(), "选择原情报表")
        res = Xlsx_File_suffix_check(file_path)
        self.ui.lineEdit.setText(res)
        self.name1 = file_path

    def pushButton_2_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(QMainWindow(), "选择新情报表")
        res = Xlsx_File_suffix_check(file_path)
        self.ui.lineEdit_3.setText(res)
        self.ui.lineEdit_2.setText("")
        self.name2 = file_path

    def pushButton_4_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(QMainWindow(), "选择结果情报表")
        res = Xlsx_File_suffix_check(file_path)
        self.ui.lineEdit_4.setText(res)
        self.name3 = file_path

    def pushButton_3_clicked(self):
        if (self.ui.lineEdit_4.text()) == "不选则默认为原情报表" or self.ui.lineEdit_4.text() == "":
            self.name3 = self.name1
        if self.name1 is None or self.name2 is None:
            self.ui.lineEdit_2.setText("有情报表未选择,请检查！")
        res = Formula.generate_or_update(self.name1, self.name2, self.name3)
        self.ui.lineEdit_2.setText(res)


def main():
    loader = QUiLoader()
    app = QApplication([])
    q = Query()
    q.ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
