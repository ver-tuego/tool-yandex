import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt


class LeaderboardApp(QMainWindow):
    def __init__(self, leaderboard_data):
        super().__init__()

        self.setWindowTitle("Leaderboard")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Clicks"])

        self.layout.addWidget(self.tableWidget)

        self.central_widget.setLayout(self.layout)

        self.load_leaderboard(leaderboard_data)

    def load_leaderboard(self, leaderboard_data):
        for row, entry in enumerate(leaderboard_data, 0):
            name = entry["name"]
            clicks = entry["clicks"]

            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(name)))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(clicks)))

            for col in range(2):
                item = self.tableWidget.item(row, col)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Disable editing


def main():
    app = QApplication(sys.argv)

    leaderboard_data = requests.get("https://sab.purpleglass.ru/yandex-projects/game/get-leaderboard").json()["items"]

    leaderboard_app = LeaderboardApp(leaderboard_data)
    leaderboard_app.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
