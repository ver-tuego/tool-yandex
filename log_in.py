 
import sys
import requests
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class LogIn(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('filemanager ui test 7.ui', self)
        self.reg_window = Reg()
        self.main_window = Main()
        self.pushButton.clicked.connect(self.check_user_first_pass)
        self.pushButton_2.clicked.connect(self.reg_open)
        self.ErrorMessage.hide()

    def check_user_first_pass(self):
        url = 'https://sab.purpleglass.ru/accounts'
        response = requests.get(url, params={"login": self.lineEdit.text(), "password": self.lineEdit_2.text()})
        if response.status_code == 404:
            self.ErrorMessage.show()
        if response.status_code == 200:
            self.main_window.show()
            self.hide()

    def reg_open(self):
        self.reg_window.show()
        self.hide()


class Reg(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('FILEMANAGER registration UI test.ui', self)
        self.main_window = Main()
        self.pushButton.clicked.connect(self.check_pass_reg)
        self.ErrorMessage_2.hide()
        self.ErrorMessage_3.hide()

    def check_pass_reg(self):
        if self.lineEdit_2.text() == self.lineEdit_3.text():
            url = 'https://sab.purpleglass.ru/accounts'
            response = requests.post(url, params={"login": self.lineEdit.text(), "password": self.lineEdit_2.text()})
            print(response.text)
            if response.status_code == 401:
                self.ErrorMessage_3.hide()
                self.ErrorMessage_2.show()

            if response.status_code == 400:
                self.ErrorMessage_2.hide()
                self.ErrorMessage_3.show()

            if response.status_code == 200:
                self.main_window.show()
                self.hide()
        else:
            print('Пароли не совпадают')


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main menu.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LogIn()
    ex.show()
    sys.exit(app.exec_())
