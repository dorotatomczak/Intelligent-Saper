import random as rand
import numpy as np


class SaperController():
    def __init__(self):
        self.sizex = 0
        self.sizey = 0
        self.board = []

    def createBoard(self, bombs, sizex, sizey):
        if bombs>sizex*sizey:
            print("Too many bombs for your board")
            return
        success = 0
        self.sizex = sizex
        self.sizey = sizey
        self.board = [[0 for x in range(sizex)] for y in range(sizey)]

        while success < bombs:
            x = rand.randint(0, sizex - 1)
            y = rand.randint(0, sizey - 1)

            if self.board[x][y] == 0:
                self.board[x][y] = -1
                success += 1

        for x in range(1, sizex - 1):
                for y in range(1, sizey - 1):
                    if self.board[x][y] == 0:
                        self.board[x][y] = (self.board[x - 1][y - 1] == -1) + (self.board[x - 1][y] == -1) + (
                            self.board[x - 1][y + 1] == -1) + \
                                           (self.board[x][
                                                y - 1] == -1) + \
                                           (self.board[
                                                x][
                                                y + 1] == -1) + \
                                           (self.board[
                                                x + 1][
                                                y - 1] == -1) + \
                                           (self.board[
                                                x + 1][
                                                y] == -1) + \
                                           (self.board[
                                                x + 1][
                                                y + 1] == -1)
        # ustalenie ilości bomb w rogach
        if self.board[0][0] == 0:
            self.board[0][0] = (self.board[1][0] == -1) + (self.board[1][1] == -1) + (self.board[0][1] == -1)

        if self.board[0][self.sizey - 1] == 0:
            self.board[0][self.sizey - 1] = (self.board[1][self.sizey - 1] == -1) + (
                self.board[1][self.sizey - 2] == -1) + (self.board[0][self.sizey - 2] == -1)

        if self.board[self.sizex - 1][0] == 0:
            self.board[self.sizex - 1][0] = (self.board[self.sizex - 2][0] == -1) + (
                self.board[self.sizex - 2][1] == -1) + (self.board[self.sizex - 1][1] == -1)

        if self.board[self.sizex - 1][self.sizey - 1] == 0:
            self.board[self.sizex - 1][self.sizey - 1] = (self.board[self.sizex - 2][self.sizey - 1] == -1) + (
                self.board[self.sizex - 2][self.sizey - 2] == -1) + (self.board[self.sizex - 1][self.sizey - 2] == -1)

        # ustalenie ilości bomb na brzegach planszy
        for x in range(1, self.sizex - 1):
            if self.board[x][0] == 0:
                self.board[x][0] = (self.board[x - 1][0] == -1) + \
                                   (self.board[x - 1][1] == -1) + \
                                   (self.board[x][1] == -1) + \
                                   (self.board[x + 1][1] == -1) + \
                                   (self.board[x + 1][0] == -1)
            if self.board[x][self.sizey - 1] == 0:
                    self.board[x][self.sizey - 1] = (self.board[x - 1][self.sizey - 1] == -1) + (self.board[x - 1][
                                                                                                     self.sizey - 2] == -1) + (
                                                    self.board[x][self.sizey - 2] == -1) + (self.board[x + 1][
                                                                                                self.sizey - 2] == -1) + (
                                                    self.board[x + 1][self.sizey - 1] == -1)

        # print(self.board)
        self.board = np.transpose(self.board)

        for x in range(1, self.sizey - 1):
            if self.board[x][0] == 0:
                self.board[x][0] = (self.board[x - 1][0] == -1) + (self.board[x - 1][1] == -1) + (self.board[x][1] == -1) + \
                          (self.board[x + 1][1] == -1) + \
                          (self.board[x + 1][0] == -1)
            if self.board[x][self.sizex - 1] == 0:
                self.board[x][self.sizex - 1] = (self.board[x - 1][self.sizex - 1] == -1) + (self.board[x - 1][self.sizex - 2] == -1) + \
                                                (self.board[x][self.sizex - 2] == -1) + (self.board[x + 1][self.sizex - 2] == -1) + \
                                                (self.board[x + 1][self.sizex - 1] == -1)

        self.board = np.transpose(self.board)



"""
saper = SaperController()
saper.createBoard(10, 10, 10)
print(saper.board)
"""
