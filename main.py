import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.loadTable()
        self.check = False
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.edit)

    def loadTable(self):
        req = f"SELECT * FROM Coffee"
        cur = self.connection.cursor()
        result = cur.execute(req).fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "название сорта", "степень обжарки",
                                                    "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def add(self, sender):
        widget = AddWidget()
        widget.exec()
        self.loadTable()

    def edit(self, sender):
        self.error.setText("")
        a = self.tableWidget.currentRow()
        if a == -1:
            self.error.setText("Данные не выбраны")
        else:
            widget = AddWidget(self.tableWidget.item(a, 0).text())
            widget.exec()
            self.loadTable()


class AddWidget(QDialog):
    def __init__(self, cur_id=-1):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.click)
        self.id = cur_id
        if self.id != -1:
            req = f"""SELECT * FROM Coffee WHERE id = {self.id}"""
            cur = self.connection.cursor()
            result = cur.execute(req).fetchall()[0]
            self.lineEdit.setText(result[1])
            self.checkBox.setChecked(True if result[2] == 1 else False)
            self.checkBox_2.setChecked(True if result[3] == 1 else False)
            self.lineEdit_2.setText(str(result[4]))
            self.lineEdit_3.setText(str(result[5]))
            self.lineEdit_4.setText(str(result[6]))

    def click(self, sender):
        self.error.setText("")
        if self.lineEdit.text():
            if self.id != -1:
                req = f"""UPDATE Coffee
                        SET name = '{self.lineEdit.text()}',
                        roast = {1 if self.checkBox.isChecked() else 0},
                        milled = {1 if self.checkBox_2.isChecked() else 0},
                        description = '{self.lineEdit_2.text()}',
                        price = {self.lineEdit_3.text()},
                        volume = {self.lineEdit_4.text()}
                        WHERE id = {self.id}"""
            else:
                req = f"""INSERT INTO Coffee(name, roast, milled, description, price, volume) 
                VALUES('{self.lineEdit.text()}', {1 if self.checkBox.isChecked() else 0}, 
{1 if self.checkBox_2.isChecked() else 0}, '{self.lineEdit_2.text()}', {self.lineEdit_3.text()}, 
{self.lineEdit_4.text()})"""

            cur = self.connection.cursor()
            result = cur.execute(req).fetchall()
            self.connection.commit()
            self.hide()
        else:
            self.error.setText("Неправильное название")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
