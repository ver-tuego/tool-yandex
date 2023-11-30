import sys
import requests
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('FILEMANAGER UI test 6.ui', self)
        self.pushButton.clicked.connect(self.check_user_first_pass)

    def check_user_first_pass(self):
        url = 'https://sab.purpleglass.ru/accounts'
        response = requests.get(url, params={"login": self.lineEdit.text(), "password": self.lineEdit_2.text()})
        if response.status_code == 404:
            print('Неправильный логин или пароль')
        if response.status_code == 200:
            print('pass')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
