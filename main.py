import sys
import requests
from random import randrange
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem, QAbstractItemView


class Name_check(QWidget):
    def __init__(self):
        super().__init__()
        self.new_window = MyWidget1()
        self.btn = QPushButton('Отправить', self)
        self.label1 = QLabel('<p style="color: rgb(240, 0, 0);">'
                             'Данное имя уже занято'
                             '</p>', self)
        self.label2 = QLabel('<p style="color: rgb(240, 0, 0);">'
                             'Ошибка на стороне сервера'
                             '</p>', self)
        self.name_input = QLineEdit(self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(500, 250)
        self.setWindowTitle('Введите имя')
        self.label1.move(1000, 1000)
        self.label2.move(1000, 1000)
        self.name_input.move(180, 90)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(208, 130)
        self.btn.clicked.connect(self.s_check)

    def s_check(self):
        nm = self.name_input.text()
        info = requests.get(f"https://sab.purpleglass.ru/yandex-projects/game/check-username?username={nm}").status_code
        print(info)
        if info == 200:
            # Открываем основную прогу
            self.new_window.show()
            # Скрываем текущее окно
            self.hide()
        if info == 403:
            self.label2.move(1000, 1000)
            self.label1.move(180, 110)
        else:
            self.label1.move(1000, 1000)
            self.label2.move(180, 110)
        self.name_input.clear()


class MyWidget1(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('project.ui', self)
        self.leaderboard_data = requests.get("https://sab.purpleglass.ru/yandex-projects/game/get-leaderboard").json()[
            "items"]
        self.initUI()
        self.a = 0
        self.table = self.findChild(QTableWidget, "tableWidget")
        self.table.setRowCount(5)
        self.table.setColumnCount(2)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 60)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.aafaw()

    def initUI(self):
        self.ClickButton.clicked.connect(self.random_tp)

    def random_tp(self):
        self.ClickButton.move(randrange(20, 310), randrange(240, 530))
        self.a += 1
        self.label.setText(f'Кол-во кликов: {self.a}')

    def aafaw(self):
        for i, item in enumerate(self.leaderboard_data):
            name_item = QTableWidgetItem(item["name"])
            clicks_item = QTableWidgetItem()
            clicks_item.setData(0, item["clicks"])

            self.table.setItem(i, 0, name_item)
            self.table.setItem(i, 1, clicks_item)

            for col in range(2):
                item = self.table.item(i, col)
                # Disable editing
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    def closeEvent(event: QCloseEvent):
        # Отправляем данные через requests
        data = {"name": "clicks"}
        response = requests.post("https://sab.purpleglass.ru/yandex-projects/game/get-leaderboard", json=data)
        if response.status_code == 200:
            print("Данные успешно отправлены")
            print('200')
        else:
            print("Ошибка при отправке данных:", response.status_code)

        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Name_check()
    ex.show()
    sys.exit(app.exec())
