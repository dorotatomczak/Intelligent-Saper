import random as rand
from Saper.SaperController import SaperController
import sys

blankid = 10
bombid = -1

class Predykaty:
    def __init__(self, saperController):
        self.sc = saperController
        self.sizey = self.sc.GetSizeY()
        self.sizex = self.sc.GetSizeX()
        self.board = [[blankid for y in range(self.sizey)] for x in range(self.sizex)]
        #  10 nieznane pole
        #  -1 przewidywana bomba

    def rewriteBoard(self):
        for i in range(0, self.sizey):
            for j in range(0, self.sizex):
                if self.board[i][j] != -1 and self.sc.covered[i][j] is False:
                    self.board[i][j] = self.sc.GetBoard()[i][j]

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
                    if self.board[i+y][j+x] == bombid:
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
                    if self.board[y+i][x+j] == blankid:
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
                        if i != 2 and j != 2 and self.board[y+i][x+j] == k:
                            bombs = self.bombNeighbour(i+y, j+x)  # bombs ile ma, k ile potrzebuje
                            blanks = self.blankNeighbour(i+y, j+x)  # blanks ile miejsca na mobmy
                            if blanks-bombs == k:
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
                    if self.board[y+i][x+j] == bombid:
                        bombs += 1
        return bombs == self.board[y][x]

    def uncoverSurroundings(self, y, x):
        pi = self.getpi(y)
        ki = 2
        pj = self.getpj(x)
        kj = 2
        for i in range(pi, ki):
            for j in range(pj, kj):
                if y + i < self.sizey and x + j < self.sizex:
                    if i != 1 or j != 1:
                        self.sc.UncoverField(i+y, j+x)
        self.rewriteBoard()

    def wyswietltablice(self):
        for i in range(0, self.sizey):
            for j in range(0, self.sizex):
                sys.stdout.write(str(self.board[i][j]))
                sys.stdout.write(" ")
            sys.stdout.write("\n")

    def start(self):  # return 2 if looped, 1 if won, -1 if lost
        y = rand.randint(0, self.sizey - 1)
        x = rand.randint(0, self.sizex - 1)
        self.sc.UncoverField(y, x)  # pierwsze odkrycie losowego pola

        if self.sc.GetState() == -1:  # powiadom main o przegranej aby mogl zliczyc
            return -1
        if self.sc.GetState() == 1:  # powiadom main o wygranej aby mogl zliczyc
            print("\n")
            self.wyswietltablice()
            self.rewriteBoard()
            print("\n")
            self.wyswietltablice()
            return 1
        while True:
            self.rewriteBoard()
            error = True
            for i in range(0, self.sizey):
                for j in range(0, self.sizex):
                    if self.board[i][j] == blankid and self.sureBomb(i, j):
                        self.board[i][j] = -1
                        error = False
                    elif self.board[i][j] != bombid and self.allBombsFound(i, j):
                        self.uncoverSurroundings(i, j)

                        error = False
            if error:
                w = 0
                q = 0
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
        self.board = [[0, 1, 1, 1, 0],
                     [0, 2, -1, 2, 0],
                     [10, 2, -1, 2, 0],
                     [10, 1, 1, 1, 0],
                     [0, 0, 0, 0, 0]]
        self.sizex = 5
        self.sizey = 5
        print(self.allBombsFound(2, 1))
        for i in range(0, self.sizey):
            for j in range(0, self.sizex):
                print(self.board[i][j])


won = 0
lost = 0
looped = 0

for index in range(0, 5):
    saper = SaperController()
    saper.createBoard(60, 15, 15)
    p = Predykaty(saper)
    x = p.start()
    if x == 1:
        won += 1
    elif x == -1:
        lost += 1
    else:
        looped += 1

print("Won:")
print(won)
print("Lost:")
print(lost)
print("Looped:")
print(looped)

# saper = SaperController()
# saper.createBoard(1, 15, 15)
# p = Predykaty(saper)
# p.test()