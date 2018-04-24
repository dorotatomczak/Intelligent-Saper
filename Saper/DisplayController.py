import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from Saper.SaperController import SaperController


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.saper = SaperController()
        self.saper.createBoard(10, 10, 10)
        self.title = 'Saper'
        self.left = 50
        self.top = 50
        self.width = 10*self.saper.sizex
        self.height = 20+10*self.saper.sizey
        self.initUI()

        newGameButton = QPushButton('New Game')
        # add to the layout
        layout.addWidget(newGameButton, 0, self.saper.sizex/2-1)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        buttons = {}

        for i in range(self.saper.sizex):
            for j in range(self.saper.sizey):
                # keep a reference to the buttons

                buttons[(i, j)] = QPushButton(str(self.saper.board[i][j]))
                # add to the layout
                layout.addWidget(buttons[(i, j)], i+1, j)

        widget.setLayout(layout)

        widget.show()
    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget()
    layout = QGridLayout()

    ex = App()
    sys.exit(app.exec_())


