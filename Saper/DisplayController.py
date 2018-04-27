import sys
import tkinter as tk

from Saper.SaperController import SaperController

class GUI():
    def __init__(self, app):
        self.master = app.master
        self.master.title(app.title)
        self.app = app
        self.square_size = 20
        self.canvas_width = app.saper.getSizeX() * self.square_size
        self.canvas_height = app.saper.getSizeY() * self.square_size

        self.covered = tk.PhotoImage(file='res/covered.gif')
        self.blank = tk.PhotoImage(file='res/blank.gif')
        self.one = tk.PhotoImage(file='res/one.gif')
        self.two = tk.PhotoImage(file='res/two.gif')
        self.three = tk.PhotoImage(file='res/three.gif')
        self.bomb = tk.PhotoImage(file='res/bomb.gif')
        self.red_bomb = tk.PhotoImage(file='res/red_bomb.gif')

        self.menu_bar = tk.Menu(self.master)
        self.menu_bar.add_command(label="New game", command=self.newGame)
        self.master.config(menu=self.menu_bar)

        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, background="grey")
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)
        self.canvas.bind("<Button-1>", self.click)
        self.fill_canvas()

        self.current_column = None
        self.current_row = None

        w = self.canvas_width
        h = self.canvas_height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def click(self, event):
        # Figure out which square we've clicked
        col_size = row_size = self.square_size
        self.current_column = int(event.x / col_size)
        self.current_row = int(event.y / row_size)

        # Odsloniecie przycisku
        self.app.saper.uncoverField(self.current_row, self.current_column)
        self.refresh()

    def newGame(self):
        self.fill_canvas()
        #dodac inicjalizacje nowej gry - TO DO

    def refresh(self):
        for row in range(self.app.saper.getSizeY()):
            for col in range(self.app.saper.getSizeX()):

                if app.saper.covered[row][col] == False:
                    x1 = (col * self.square_size)
                    y1 = (row * self.square_size)
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
                    self.canvas.create_image(x1, y1, image=image, anchor=tk.NW)

    def fill_canvas(self):
        for row in range(self.app.saper.getSizeY()):
            for col in range(self.app.saper.getSizeX()):
                x1 = (col * self.square_size)
                y1 = (row * self.square_size)
                self.canvas.create_image(x1, y1, image=self.covered, anchor=tk.NW)


class App():

    def __init__(self, master):
        self.saper = SaperController()
        self.saper.createBoard(10, 10, 10)
        self.title = 'Saper'
        self.master = master
        self.gui = GUI(self)


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(width=False, height=False)
    app = App(root)
    root.mainloop()


