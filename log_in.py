import sys
import requests
import configparser
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QFileDialog


config = configparser.ConfigParser()
config.read('config.ini')
if config['DEFAULT']['token'] == '':
    a = False
else:
    a = True


class LogIn(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('filemanager ui test 7.ui', self)
        self.reg_window = Reg()
        self.main_window = Main()
        self.pushButton.clicked.connect(self.check_user_first_pass)
        self.pushButton_2.clicked.connect(self.reg_open)
        self.ErrorMessage.hide()
        self.lineEdit_2.setEchoMode(QLineEdit.Password)

    def log_skip(self):
        self.main_window.show()
        self.hide()

    def check_user_first_pass(self):
        url = 'https://sab.purpleglass.ru/accounts'
        response = requests.get(url, params={"login": (login := self.lineEdit.text()), "password": (password := self.lineEdit_2.text())})
        if response.status_code == 404:
            self.ErrorMessage.show()
        if response.status_code == 200:
            token = response.json()["token"]
            config['DEFAULT'] = {'login': login,
                                 'password': password,
                                 'token': token}
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            self.main_window.show()
            self.hide()

    def reg_open(self):
        self.reg_window.show()
        self.hide()


class Reg(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('FILEMANAGER registration UI test (1).ui', self)
        self.main_window = Main()
        self.pushButton.clicked.connect(self.check_pass_reg)
        self.ErrorMessage_2.hide()
        self.ErrorMessage_3.hide()
        self.ErrorMessage_4.hide()
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_3.setEchoMode(QLineEdit.Password)

    def check_pass_reg(self):
        if self.lineEdit_2.text() == self.lineEdit_3.text():
            url = 'https://sab.purpleglass.ru/accounts'
            response = requests.post(url, params={"login": (login := self.lineEdit.text()), "password": (password := self.lineEdit_2.text())})
            if response.status_code == 401:
                self.ErrorMessage_3.hide()
                self.ErrorMessage_4.hide()
                self.ErrorMessage_2.show()
            if response.status_code == 400:
                self.ErrorMessage_2.hide()
                self.ErrorMessage_4.hide()
                self.ErrorMessage_3.show()
            if response.status_code == 200:
                token = response.json()["token"]
                config['DEFAULT'] = {'login': login,
                                     'password': password,
                                     'token': token}
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                self.main_window.show()
                self.hide()
        else:
            self.ErrorMessage_2.hide()
            self.ErrorMessage_3.hide()
            self.ErrorMessage_4.show()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main menu inactive buttons.ui', self)
        self.acc_window = AccSettings()
        self.AddButton_2.setEnabled(False)
        self.AddButton_4.setEnabled(False)
        self.AddButton_3.setEnabled(False)
        self.pushButton_3.clicked.connect(self.settings_open)
        self.AddButton.clicked.connect(self.add_file)
        url = 'https://sab.purpleglass.ru/uploads/files'
        response = requests.get(url, params={"token": "d4988409b7253d49375043dedb118b13"})
        print(response.text)


        # Создать модель списка, добавить данные
        slm=QStringListModel()
        self.qList = ['1', '2', '3', '4']

        # Установить вид списка моделей, загрузить список данных
        slm.setStringList(self.qList)

        # Установите модель представления списка
        self.listView.setModel(slm)

        # Нажмите, чтобы активировать пользовательский слот
        self.listView.clicked.connect(self.clicked)

    def clicked(self):
        print("HUYY")

    def settings_open(self):
        self.acc_window.show()
        self.hide()
        self.acc_window.update_values()

    def add_file(self):
        file, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", "All Files (*)")
        print(file)
        url = 'https://sab.purpleglass.ru/upload'
        files = {'file': (file, open(file, 'rb'))}
        config.read('config.ini')
        response = requests.post(url, files=files, params={"token": config['DEFAULT']['token'], "private": 1})


class AccSettings(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('AccSetings.ui', self)
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.pushButton_2.clicked.connect(self.settings_close)
        self.pushButton.clicked.connect(self.acc_exit)
        self.checkBox.stateChanged.connect(self.password_show)
        self.checkBox_2.stateChanged.connect(self.token_show)

    def password_show(self, state):
        if QtCore.Qt.Checked == state:
            self.lineEdit_2.setEchoMode(QLineEdit.Normal)
        else:
            self.lineEdit_2.setEchoMode(QLineEdit.Password)

    def token_show(self, state):
        if QtCore.Qt.Checked == state:
            config.read('config.ini')
            self.checkBox_2.setText(f"Показать токен: {config['DEFAULT']['token']}")
        else:
            self.checkBox_2.setText('Показать токен:')

    def settings_close(self):
        self.main_window = Main()
        self.main_window.show()
        self.hide()

    def acc_exit(self):
        self.login_window = LogIn()
        self.login_window.show()
        self.hide()

    def update_values(self):
        config.read('config.ini')
        self.lineEdit.setText(config['DEFAULT']['login'])
        self.lineEdit_2.setText(config['DEFAULT']['password'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if a:
        ex = Main()
    else:
        ex = LogIn()
    ex.show()
    sys.exit(app.exec_())
