import sys
import requests
import configparser
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QFileDialog, QListWidgetItem


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
            with open('../config.ini', 'w') as configfile:
                config.write(configfile)
            self.main_window.show()
            self.main_window.parsed_items()
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
                with open('../config.ini', 'w') as configfile:
                    config.write(configfile)
                self.main_window.show()
                self.main_window.parsed_items()
                self.hide()
        else:
            self.ErrorMessage_2.hide()
            self.ErrorMessage_3.hide()
            self.ErrorMessage_4.show()


class Main(QMainWindow):

    items = []
    current_item = None

    def __init__(self):
        super().__init__()
        uic.loadUi('main menu v8.1.ui', self)
        self.acc_window = AccSettings()
        self.AddButton_4.setEnabled(False)
        self.AddButton_3.setEnabled(False)
        self.AddButton_4.clicked.connect(self.delete_item)
        self.AddButton_3.clicked.connect(self.download_item)
        self.pushButton_3.clicked.connect(self.settings_open)
        self.AddButton.clicked.connect(self.add_file)
        self.listWidget.itemClicked.connect(self.item_clicked)

    def item_clicked(self, item):
        url = item.data(1)

        for json_item in self.items['items']:
            if json_item['url'] == url:
                self.current_item = json_item
        print(self.current_item)
        self.AddButton_3.setStyleSheet("""QPushButton {
            background-color: #292929;
            border-radius: 25px;
            border: 2px solid #808080;
            color: rgb(255, 255, 255);
        }

        QPushButton:hover {
            background-color: #ffa31a;
        }""")
        self.AddButton_3.setEnabled(True)
        self.AddButton_4.setStyleSheet("""QPushButton {
            background-color: #292929;
            border-radius: 25px;
            border: 2px solid #808080;
            color: rgb(255, 255, 255);
        }

        QPushButton:hover {
            background-color: #ffa31a;
        }""")
        self.AddButton_4.setEnabled(True)

    def delete_item(self):
        url = "http://sab.purpleglass.ru/uploads/files"
        response = requests.delete(url, params={"token": config['DEFAULT']['token'], "file_id": self.current_item['file_id']})
        self.items = []
        self.parsed_items()
        self.update()

    def download_item(self):
        url = f"http://sab.purpleglass.ru/uploads/{self.current_item['file_name']}"
        response = requests.get(url, params={"token": config['DEFAULT']['token']})
        with open(self.current_item['file_name'][11::], 'wb') as f:
            f.write(response.content)

    def parsed_items(self):
        url = 'https://sab.purpleglass.ru/uploads/files'
        response = requests.get(url, params={"token": config['DEFAULT']['token']})
        self.items = response.json()
        for item in self.items['items']:
            self.render_item(item)


    def render_item(self, item):
        file_name = item['file_name']
        url = item['url']
        size = item['size']
        private = item['private']
        list_item = QListWidgetItem()
        list_item.setText(f"File: {file_name[11::]}\nSize: {size} Bytes\nPrivate: {'Yes' if private else 'No'}")
        list_item.setData(1, url)
        list_item.setSizeHint(list_item.sizeHint())
        self.listWidget.addItem(list_item)

    def settings_open(self):
        self.acc_window.show()
        self.hide()
        self.acc_window.update_values()

    def add_file(self):
        file, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", "All Files (*)")
        if file != '':
            url = 'https://sab.purpleglass.ru/upload'
            files = {'file': (file, open(file, 'rb'))}
            config.read('config.ini')
            gg = requests.post(url, files=files, params={"token": config['DEFAULT']['token'], "private": 1})
            self.items['items'].append(gg.json())
            self.render_item(gg.json())


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
        self.main_window.parsed_items()
        self.hide()

    def acc_exit(self):
        config['DEFAULT'] = {'login': '',
                             'password': '',
                             'token': ''}
        with open('../config.ini', 'w') as configfile:
            config.write(configfile)
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
        ex.parsed_items()
    else:
        ex = LogIn()
    ex.show()
    sys.exit(app.exec_())
