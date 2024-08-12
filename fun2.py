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
        self.name2 = file_path

    def pushButton_4_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(QMainWindow(), "选择结果情报表")
        res = Xlsx_File_suffix_check(file_path)
        self.ui.lineEdit_4.setText(res)
        self.name3 = file_path

    def pushButton_3_clicked(self):
        self.ui.textEdit.setPlainText("")
        if (self.ui.lineEdit_4.text()) == "不选则默认为原情报表" or self.ui.lineEdit_4.text() == "":
            self.name3 = self.name1
        if self.name1 is None or self.name2 is None:
            self.ui.textEdit.setPlainText("\t" + "有情报表未选择,请检查！")
        QTimer.singleShot(100, lambda: self.display_result())

    def display_result(self):
        time1 = Formula.generate_or_update(self.name1, self.name2, self.name3)  #int型
        self.ui.textEdit.setPlainText("\t" + "情报表更新完成!总用时" + str(time1) + "s")
        QTimer.singleShot(1000, lambda: self.display_result1(time1))

    def display_result1(self, time):
        if self.name1 == self.name3 and self.name3.split("/")[-1] != 'Inte-All.xlsx':
            self.ui.textEdit.append("\t" + "下面开始更新总表")
            QTimer.singleShot(100, lambda: self.display_result2(time))

    def display_result2(self, time):
        # 大前提,必须是更新操作。如果是开新表不执行操作
        # 更新也可能是更新总表,所以需要再次判断确定更新的不是总表
        time2 = Formula.generate_or_update('Inte-All.xlsx', self.name2, 'Inte-All.xlsx')
        self.ui.textEdit.append("\t" + "总表更新完成!总用时" + str(time2 + time) + "s")
        pass


def main():
    loader = QUiLoader()
    app = QApplication([])
    q = Query()
    q.ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
