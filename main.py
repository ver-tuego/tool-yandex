import sys
import requests
from random import randrange
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.initUI()
        self.a = 0

    def initUI(self):
        self.ClickButton.clicked.connect(self.random_tp)

    def random_tp(self):
        self.ClickButton.move(randrange(20, 310), randrange(240, 530))
        self.a += 1
        self.label.setText(f'Кол-во кликов: {self.a}')


class Name_check(QWidget):
    def __init__(self):
        super().__init__()
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
        name = self.name_input.text()
        info = requests.get(f"https://sab.purpleglass.ru/yandex-projects/game/check-username?username={name}").status_code
        print(info)
        if info == 200:
            self.new_window = MyWidget1()
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
        uic.loadUi('untitled.ui', self)
        self.initUI()
        self.a = 0

    def initUI(self):
        self.ClickButton.clicked.connect(self.random_tp)

    def random_tp(self):
        self.ClickButton.move(randrange(20, 310), randrange(240, 530))
        self.a += 1
        self.label.setText(f'Кол-во кликов: {self.a}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    print(app)
    ex = Name_check()
    ex.show()
    sys.exit(app.exec())
