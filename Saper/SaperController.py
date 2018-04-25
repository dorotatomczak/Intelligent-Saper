# coding=utf-8
import random as rand
import numpy as np


class SaperController():
    def __init__(self):
        self.sizex = 0
        self.sizey = 0
        self.board = []

    def getSizeX(self):
        return self.sizex

    def getSizeY(self):
        return self.sizey


    def createBoard(self, bombs, sizex, sizey):
        if bombs>sizex*sizey:
            print("Too many bombs for your board")
            return
        success = 0
        self.sizex = sizex
        self.sizey = sizey
        self.board = [[0 for y in range(sizey)] for x in range(sizex)]
        self.covered = [[True for y in range(sizey)] for x in range(sizex)]
        self.outBoard = [[" " for y in range(sizey)] for x in range(sizex)]

        while success < bombs:
            x = rand.randint(0, sizex - 1)
            y = rand.randint(0, sizey - 1)

            if self.board[x][y] == 0:
                self.board[x][y] = -1
                success += 1

        for x in range(1, sizex - 1):
                for y in range(1, sizey - 1):
                    if self.board[x][y] == 0:
                        self.board[x][y] = int(self.board[x - 1][y - 1] == -1) + (self.board[x - 1][y] == -1) + (
                            self.board[x - 1][y + 1] == -1) + (self.board[x][y - 1] == -1) + \
                                           (self.board[x][y + 1] == -1) + (self.board[x + 1][y - 1] == -1) + \
                                           (self.board[x + 1][y] == -1) + (self.board[x + 1][y + 1] == -1)
        # ustalenie ilości bomb w rogach
        if self.board[0][0] == 0:
            self.board[0][0] = int(self.board[1][0] == -1) + (self.board[1][1] == -1) + (self.board[0][1] == -1)

        if self.board[0][self.sizey - 1] == 0:
            self.board[0][self.sizey - 1] = int(self.board[1][self.sizey - 1] == -1) + (
                self.board[1][self.sizey - 2] == -1) + (self.board[0][self.sizey - 2] == -1)

        if self.board[self.sizex - 1][0] == 0:
            self.board[self.sizex - 1][0] = int(self.board[self.sizex - 2][0] == -1) + (
                self.board[self.sizex - 2][1] == -1) + (self.board[self.sizex - 1][1] == -1)

        if self.board[self.sizex - 1][self.sizey - 1] == 0:
            self.board[self.sizex - 1][self.sizey - 1] = int(self.board[self.sizex - 2][self.sizey - 1] == -1) + (
                self.board[self.sizex - 2][self.sizey - 2] == -1) + (self.board[self.sizex - 1][self.sizey - 2] == -1)

        # ustalenie ilości bomb na brzegach planszy
        for x in range(1, self.sizex - 1):
            if self.board[x][0] == 0:
                self.board[x][0] = int(self.board[x - 1][0] == -1) + \
                                   (self.board[x - 1][1] == -1) + \
                                   (self.board[x][1] == -1) + \
                                   (self.board[x + 1][1] == -1) + \
                                   (self.board[x + 1][0] == -1)
            if self.board[x][self.sizey - 1] == 0:
                    self.board[x][self.sizey - 1] = int(self.board[x - 1][self.sizey - 1] == -1) + (self.board[x - 1][
                                                                                                     self.sizey - 2] == -1) + (
                                                    self.board[x][self.sizey - 2] == -1) + (self.board[x + 1][
                                                                                                self.sizey - 2] == -1) + (
                                                    self.board[x + 1][self.sizey - 1] == -1)

        self.board = np.transpose(self.board)
        for y in range(1, self.sizey - 1):
            if self.board[y][0] == 0:
                self.board[y][0] = int(self.board[y - 1][0] == -1) + (self.board[y - 1][1] == -1) + (self.board[y][1] == -1) + \
                          (self.board[y + 1][1] == -1) + (self.board[y + 1][0] == -1)

            if self.board[y][self.sizex - 1] == 0:
                self.board[y][self.sizex - 1] = int(self.board[y - 1][self.sizex - 1] == -1) + (self.board[y - 1][self.sizex - 2] == -1) + \
                                                (self.board[y][self.sizex - 2] == -1) + (self.board[y + 1][self.sizex - 2] == -1) + \
                                                (self.board[y + 1][self.sizex - 1] == -1)


        self.board = np.transpose(self.board)

    def uncoverField(self, x, y):
        if self.covered[x][y] == True:
            self.covered[x][y]=False
            if self.board[x][y] == 0:
                if x>0:
                    self.uncoverField(x-1,y)
                if y>0:
                    self.uncoverField(x,y-1)
                if x>0 and y>0:
                    self.uncoverField(x-1,y-1)
                if x<self.sizex-1:
                    self.uncoverField(x+1,y)
                if y<self.sizey-1:
                    self.uncoverField(x,y+1)
                if x<self.sizex-1 and y<self.sizey-1:
                    self.uncoverField(x+1,y+1)
                if x>0 and y<self.sizey-1:
                    self.uncoverField(x-1,y+1)
                if x<self.sizex-1 and y>0:
                    self.uncoverField(x+1,y-1)

        for x in range(0, self.sizex):
                for y in range(0, self.sizey):
                    if self.covered[x][y]==False:
                        self.outBoard[x][y]=self.board[x][y]

        #transpose, żeby w konsoli wyświetlało rząd pod rzędem jako tablicę z numpy. Można potem usunąć
        self.outBoard=np.transpose(self.outBoard)
        self.outBoard=np.transpose(self.outBoard)

    def GetSizeX(self):
        return self.sizex

    def GetSizeY(self):
        return self.sizey

    def GetBoard(self):
        return self.outBoard



saper = SaperController()
saper.createBoard(5, 10, 10)
print(saper.board)
print(saper.GetBoard())
