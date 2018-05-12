import random as rand
from Saper.SaperController import SaperController
import sys
import time

blankid = 10
bombid = -1

class Predykaty:
    def __init__(self, app):
        self.sc = app.saper
        self.gui = app.gui
        self.sizex = self.sc.GetSizeY() # changed because of making a mistake in axis
        self.sizey = self.sc.GetSizeX()
        # self.board = [[blankid for y in range(self.sizey)] for x in range(self.sizex)]
        #  10 nieznane pole
        #  -1 przewidywana bomba

    def rewriteBoard(self):
        for i in range(0, self.sizey):
            for j in range(0, self.sizex):
                if self.sc.outBoard[i][j] != -1 and self.sc.covered[i][j] is False:
                    self.sc.outBoard[i][j] = self.sc.GetBoard()[i][j]

    def getpi(self, y):
        if y > 0:
            return -1
        else:
            return 0

    def getpj(self, x):
        if x > 0:
            return -1
        else:
            return 0


    def bombNeighbour(self, y, x):
        bombs = 0
        pi = self.getpi(y)
        ki = 2
        pj = self.getpj(x)
        kj = 2
        for i in range(pi, ki):
            for j in range(pj, kj):
                if y + i < self.sizey and x + j < self.sizex:
                    if self.sc.outBoard[i+y][j+x] == bombid:
                        bombs += 1
        return bombs

    def blankNeighbour(self, y, x):
        blanks = 0
        pi = self.getpi(y)
        ki = 2
        pj = self.getpj(x)
        kj = 2
        for i in range(pi, ki):
            for j in range(pj, kj):
                if y + i < self.sizey and x + j < self.sizex:
                    if self.sc.outBoard[y+i][x+j] == blankid:
                        blanks += 1
        return blanks

    def sureBomb(self, y, x):  # i,j którą komorkę sprawdzamy, predykat czy board[i][j] jest bombą
        pi = self.getpi(y)
        ki = 2
        pj = self.getpj(x)
        kj = 2
        for k in range(0, 8):  # szukamy po bokach od najmniejszej liczby
            for i in range(pi, ki):
                for j in range(pj, kj):
                    if y + i < self.sizey and x + j < self.sizex:
                        if self.sc.outBoard[y+i][x+j] == k:
                            bombs = self.bombNeighbour(i+y, j+x)  # bombs ile ma, k ile potrzebuje
                            blanks = self.blankNeighbour(i+y, j+x)  # blanks ile miejsca na mobmy
                            if blanks+bombs == k:
                                return True
        return False

    def allBombsFound(self, y, x):  # znamy polozenie bomb dookola mozemy odkryc to co zostalo
        bombs = 0  # juz zgadniete bomby
        pi = self.getpi(y)
        ki = 2
        pj = self.getpj(x)
        kj = 2
        for i in range(pi, ki):  # jesli jest miejsce to to pojdzie od -1 do 1 nie ma jesli
            for j in range(pj, kj):
                if y+i < self.sizey and x+j < self.sizex:
                    if self.sc.outBoard[y+i][x+j] == bombid:
                        bombs += 1
        return bombs == self.sc.outBoard[y][x]

    def uncoverSurroundings(self, y, x):
        pi = self.getpi(y)
        ki = 2
        pj = self.getpj(x)
        kj = 2
        error = True
        for i in range(pi, ki):
            for j in range(pj, kj):
                if y + i < self.sizey and x + j < self.sizex:
                    if self.sc.outBoard[i+y][j+x] != bombid and self.sc.covered[i+y][j+x]:
                        self.sc.UncoverField(i+y, j+x)
                        error = False
        return error

    def wyswietltablice(self):
        for i in range(0, self.sizey):
            for j in range(0, self.sizex):
                sys.stdout.write(str(self.sc.outBoard[i][j]))
                sys.stdout.write(" ")
            sys.stdout.write("\n")

    def start(self):  # return 2 if looped, 1 if won, -1 if lost
        y = rand.randint(0, self.sizey - 2)
        x = rand.randint(0, self.sizex - 2)
        self.sc.UncoverField(y, x)  # pierwsze odkrycie losowego pola
        if self.sc.GetState() == -1:  # powiadom main o przegranej aby mogl zliczyc
            return 3
        if self.sc.GetState() == 1:  # powiadom main o wygranej aby mogl zliczyc
            return 1
        while True:
            error = True
            for i in range(0, self.sizey):
                for j in range(0, self.sizex):
                    if self.sc.outBoard[i][j] == blankid and self.sureBomb(i, j):
                        self.sc.outBoard[i][j] = bombid
                        error = False
                    elif self.sc.outBoard[i][j] != bombid and self.allBombsFound(i, j):
                        error = self.uncoverSurroundings(i, j)
            if error:
                # return 2
                w = 0
                q = 0
                flag1 = False
                for k in range(0, 100):
                    q = rand.randint(0, self.sizey - 1)
                    w = rand.randint(0, self.sizex - 1)
                    if self.sc.GetBoard()[q][w] == blankid and flag1 is False:
                        flag1 = True
                if flag1 is False:
                    flag = True
                    for i in range(0, self.sizey):
                        for j in range(0, self.sizex):
                            if self.sc.GetBoard()[i][j] == blankid and flag is True:
                                q = i
                                w = j
                                flag = False
                self.sc.UncoverField(q, w)
            if self.sc.GetState() == -1:  # powiadom main o przegranej aby mogl zliczyc
                return -1
            if self.sc.GetState() == 1:  # powiadom main o wygranej aby mogl zliczyc
                return 1

    def test(self):
        self.sc.outBoard = [[0, 1, 1, 1, 0],
                     [0, 2, -1, 2, 0],
                     [10, 2, -1, 2, 0],
                     [10, 1, 1, 1, 0],
                     [0, 0, 0, 0, 0]]
        self.sizex = 5
        self.sizey = 5
        print(self.allBombsFound(2, 1))
        for i in range(0, self.sizey):
            for j in range(0, self.sizex):
                print(self.sc.outBoard[i][j])

    def play(self, settings=None):
        if settings is None:
            num_iters = 100
            min_height = 10
            max_height = 10
            min_width = 10
            max_width = 10
            min_bombs = 7
            max_bombs = 11
        else:
            num_iters = settings['Games']
            min_height = settings['minHeight']
            max_height = settings['maxHeight']
            min_width = settings['minWidth']
            max_width = settings['maxWidth']
            min_bombs = settings['minBombs']
            max_bombs = settings['maxBombs']
            won = 0
            lost = 0
            looped = 0
            firstmove = 0

        for i in range(0, num_iters):
            bombs = rand.randint(min_bombs, max_bombs)
            width = rand.randint(min_width, max_width)
            height = rand.randint(min_height, max_height)
            self.sc.createBoard(bombs, width, height)
            self.sizey = self.sc.GetSizeY() # when initialize predykaty board not created yet
            self.sizex = self.sc.GetSizeX()
            self.gui.update_info(
                "Method: Neural Network\nGame:" + str(i+1) + "\nWin count:" + str(won) + "\nLost count:" + str(lost)
                + "\nLooped count:" + str(looped) + "\nFirst move count: " + str(firstmove))
            self.gui.refresh()
            x = self.start()
            if x == 1:
                won += 1
            elif x == -1:
                lost += 1
            elif x == 3:
                firstmove += 1
            else:
                looped += 1
            self.gui.update_info(
                "Method: Neural Network\nGame:" + str(i+1) + "\nWin count:" + str(won) + "\nLost count:" + str(lost)
                + "\nLooped count:" + str(looped) + "\nFirst move count: " + str(firstmove))
            self.gui.refresh()

"""won = 0
lost = 0
looped = 0
firstmove = 0

for index in range(0, 100):
    saper = SaperController()
    saper.createBoard(10, 15, 15)
    p = Predykaty(saper)
    x = p.start()
    if x == 1:
        won += 1
        print("Won")
    elif x == -1:
        lost += 1
        print("Lost")
    elif x == 3:
        firstmove += 1
        print("First move")
    else:
        looped += 1
        print("Looped")

print("Won:")
print(won)
print("Lost:")
print(lost)
print("Looped:")
print(looped)
print("First move:")
print(firstmove)"""

# saper = SaperController()
# saper.createBoard(1, 15, 15)
# p = Predykaty(saper)
# p.test()