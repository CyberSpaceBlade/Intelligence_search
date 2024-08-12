import os
import sys
import ipaddress
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import *
import Formula


def is_ipv4(ip):
    try:
        return str(ipaddress.IPv4Address(ip))
    except:
        pass


def display_result(file_path):
    os.system(file_path)


def Xlsx_File_suffix_check(file_path):
    excel_name = file_path.split("/")[-1]
    suffix = str(excel_name).split(".")[-1]
    if suffix != "xlsx":
        res = "请选择xlsx格式的情报表!"
    else:
        res = excel_name
    return res


def Txt_File_suffix_check(file_path):
    excel_name = file_path.split("/")[-1]
    suffix = str(excel_name).split(".")[-1]
    if suffix != "txt":
        res = "请选择txt格式的情报表!"
    else:
        res = excel_name
    return res


class Query(QObject):
    def __init__(self, parent=None):
        super(Query, self).__init__(parent)
        self.name2 = None
        self.name1 = None
        self.ui = QUiLoader().load('UI/Fun3.ui')
        self.ui.pushButton.clicked.connect(self.pushButton_clicked)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_clicked)

    def pushButton_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(QMainWindow(), "选择源情报表")
        res = Xlsx_File_suffix_check(file_path)
        self.ui.lineEdit.setText(res)
        self.name1 = file_path

    def pushButton_2_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(QMainWindow(), "选择待查询文件")
        res = Txt_File_suffix_check(file_path)
        self.ui.lineEdit_3.setText(res)
        self.ui.lineEdit_2.setText("")
        self.name2 = file_path

    def pushButton_3_clicked(self):
        self.ui.lineEdit_2.setText("")
        QTimer.singleShot(100, lambda: self.display_result())

    def display_result(self):
        if self.name1 is None:
            self.ui.lineEdit_2.setText("未设定情报表!")
        elif self.name2 is None:
            self.ui.lineEdit_2.setText("未设定IP查询文件!")
        new_excel_name = self.name2.split("/")[-1]
        with open(self.name2, "r", encoding='UTF-8') as f:
            ips = f.readlines()

        ips = [is_ipv4(line.strip()) for line in ips if line.strip() and is_ipv4(line.strip()) is not None]
        # 此时的IPS里只有IP,无中文
        res = set(Formula.ips_search(ips, self.name1))  #只是肯定没有命中情报,但不排除是因为格式原因被剔除的可能
        mingzhong = set([ip for ip in ips if ip not in res])  #已命中则不再变动

        error = [ip for ip in res if Formula.IPv4_check(ip) == False]
        for error_ip in error:
            res.remove(error_ip)

        with open(self.name2, "a", encoding='UTF-8') as f:
            f.write("\n" * 2 + "共计" + str(len(mingzhong)) + "个IP命中情报" + "\n")
            if len(mingzhong) > 0:
                f.write("命中情报的IP为:" + "\n")
                for ip in mingzhong:
                    f.write(str(ip)+"\n")
            f.write("\n")

            f.write("共计" + str(len(res)) + "个IP格式正确但未命中情报" + "\n")
            if len(res) > 0:
                f.write("未命中情报的IP为:" + "\n")
                for ip in res:
                    f.write(str(ip) + "\n")
            f.write("\n")

            f.write("共计" + str(len(error)) + "个IP格式错误" + "\n")
            if len(error) > 0:
                f.write("格式错误的IP为:" + "\n")
                for ip in error:
                    f.write(str(ip) + "\n")

        f.close()
        self.ui.lineEdit_2.setText("结果在" + new_excel_name + "末尾,请查看!")
        QTimer.singleShot(500, lambda: display_result(self.name2))



def main():
    loader = QUiLoader()
    app = QApplication([])
    q = Query()
    q.ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
