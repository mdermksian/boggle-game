import sys
import time

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QGridLayout, \
    QApplication, QSizePolicy

from boggle_engine import GameType, GAME_NAMES, make_game


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.wid = 850
        self.hei = 950
        self.game_type = GameType.CLASSIC
        self.board = make_game(self.game_type)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Boggle Game")
        self.setStyleSheet("background-color: blue")

        self.game_type_options = QComboBox()
        self.game_type_options.addItems(GAME_NAMES)
        self.game_type_options.activated.connect(self.set_game_type)
        self.make_game_button = QPushButton("Make Game", self)
        self.make_game_button.setStyleSheet("color: white; font-weight: bold; font-size:24px;")
        self.make_game_button.clicked.connect(self.make_and_draw_game)

        outerlayout = QVBoxLayout()
        top_portion = QHBoxLayout()
        choices = QVBoxLayout()
        choices_label = QLabel("Board Types: ")
        choices_label.setStyleSheet("color: white; font-weight: bold;")
        choices.addWidget(choices_label)
        choices.addWidget(self.game_type_options)

        self.timer = QTimer()
        self.timer.timeout.connect(self.decrement_timer)
        self.time = 0
        self.clock = QLabel(time.strftime('%M:%S', time.gmtime(self.time)))
        self.clock.setStyleSheet("color: white; font-weight: bold; font-size: 48px;")
        self.clock.setAlignment(Qt.AlignCenter)

        top_portion.addLayout(choices)
        top_portion.addWidget(self.clock)
        top_portion.addWidget(self.make_game_button)
        self.board_portion = QGridLayout()

        outerlayout.addLayout(top_portion)
        outerlayout.addLayout(self.board_portion)
        self.setLayout(outerlayout)
        self.setGeometry(0, 0, self.wid, self.hei)
        self.show()

    def decrement_timer(self):
        self.clock.setText(time.strftime('%M:%S', time.gmtime(self.time)))
        if self.time > 0:
            self.time -= 1
        else:
            self.setStyleSheet("background-color:red;")
            self.timer.stop()

    def set_game_type(self):
        self.game_type = self.game_type_options.currentIndex()  # Press Ctrl+F8 to toggle the breakpoint.

    def make_and_draw_game(self):
        for i in reversed(range(self.board_portion.count())):
            self.board_portion.itemAt(i).widget().setParent(None)

        self.board = make_game(self.game_type)
        for i in range(self.board.size):
            for j in range(self.board.size):
                ind = i * self.board.size + j
                widget = QLabel(self.board.board_string[ind])

                widget.setStyleSheet(
                    "background-color: white; font-weight: bold; font-size: 72px; border-radius: 20%; padding: auto; text-align: center;")
                widget.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
                widget.setAlignment(Qt.AlignCenter)
                self.board_portion.addWidget(widget, i, j)

        self.time = 180
        self.timer.start(1000)
        self.setStyleSheet("background-color: blue;")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Main()
    sys.exit(app.exec_())
