from tkinter import *
from Saper.Dialog import *
from Saper.SaperController import SaperController
from Saper.Player import Player
from Saper.Predykaty import Predykaty
import time


class GUI:
    def __init__(self, app):
        self.master = app.master
        self.master.title(app.title)
        self.app = app
        self.square_size = 20
        self.canvas_width = 200
        self.canvas_height = 200

        self.covered = PhotoImage(file='res/covered.gif')
        self.blank = PhotoImage(file='res/blank.gif')
        self.one = PhotoImage(file='res/one.gif')
        self.two = PhotoImage(file='res/two.gif')
        self.three = PhotoImage(file='res/three.gif')
        self.bomb = PhotoImage(file='res/bomb.gif')
        self.red_bomb = PhotoImage(file='res/red_bomb.gif')

        self.menu_bar = Menu(self.master)
        self.menu_bar.add_command(label="Play", command=self.trainSaper)
        self.master.config(menu=self.menu_bar)

        self.canvas = Canvas(self.master, width=self.canvas_width, height=self.canvas_height, background="grey")
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)

        self.text = Text(self.master, width=1, height=80)
        self.text.insert(INSERT, "")
        self.text.pack(fill=BOTH, expand=1)

        self.resizeWindow()

    def loadNewBoard(self):
        self.canvas.delete("all")
        self.canvas_width = self.app.saper.GetSizeX() * self.square_size
        self.canvas_height = self.app.saper.GetSizeY() * self.square_size
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)

        self.fill_canvas()

        self.resizeWindow()

        self.master.update()
        # time.sleep(1)

    def resizeWindow(self):
        w = self.canvas_width
        h = self.canvas_height + 80
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))  # set window size and place in the center

    def trainSaper(self):
        d = TrainingSettingsDialog(self.master)
        if not d.canceled:
            if d.predicates_method:
                self.app.predicates.play(settings=d.result)
            else:
                self.app.player.train(settings=d.result)

    def refresh(self):
        self.fill_canvas()
        for row in range(self.app.saper.GetSizeX()):
            for col in range(self.app.saper.GetSizeY()):

                if not app.saper.covered[row][col]:
                    x1 = (row * self.square_size)
                    y1 = (col * self.square_size)

                    if self.app.saper.board[row][col] == -1:
                        image = self.red_bomb
                    elif self.app.saper.board[row][col] == 1:
                        image = self.one
                    elif self.app.saper.board[row][col] == 2:
                        image = self.two
                    elif self.app.saper.board[row][col] == 3:
                        image = self.three
                    else:
                        image = self.blank
                    self.canvas.create_image(x1, y1, image=image, anchor=NW)
                elif self.app.saper.outBoard[row][col] == -1:
                    x1 = (row * self.square_size)
                    y1 = (col * self.square_size)
                    image = self.bomb
                    self.canvas.create_image(x1, y1, image=image, anchor=NW)


        self.master.update()
        time.sleep(1)

    def update_info(self, new_info):
        self.text.delete("1.0", END)
        self.text.insert(END, new_info)

    def fill_canvas(self):
        for row in range(self.app.saper.GetSizeX()):
            for col in range(self.app.saper.GetSizeY()):
                x1 = (row * self.square_size)
                y1 = (col * self.square_size)
                self.canvas.create_image(x1, y1, image=self.covered, anchor=NW)


class App:
    def __init__(self, master):
        self.saper = SaperController()
        self.title = 'Saper'
        self.master = master
        self.gui = GUI(self)
        self.player = Player(self)
        self.predicates = Predykaty(self)


if __name__ == '__main__':
    root = Tk()
    root.minsize(200, 250)
    root.resizable(width=True, height=True)
    app = App(root)
    root.mainloop()
