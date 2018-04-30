import numpy as np
from Saper.SaperController import SaperController

class Player:
    def __init__(self, saperController):
        self.sc = saperController
        self.oneBoardSize = 4
        self.hiddenLayerSize = 50

        self.params = {}
        self.params['W1'] = np.random.randn(self.oneBoardSize**2, self.hiddenLayerSize) * 0.001
        self.params['b1'] = np.zeros(self.hiddenLayerSize)
        self.params['W2'] = np.random.randn(self.hiddenLayerSize, self.oneBoardSize**2) * 0.001
        self.params['b2'] = np.zeros(self.oneBoardSize**2)


    def PrepareData(self):
        board = self.sc.GetBoard()
        board = np.array(board)

        self.X = self.reshape(board)

        self.y = np.array(self.sc.GetBoard())

        for i in range(0, self.sc.GetSizeX()):
            for j in range(0, self.sc.GetSizeY()):
                self.y[i,j] = int (self.sc.GetValueAt(i,j) == -1)

        self.y = self.reshape(self.y)
        print(self.X)

    def reshape(self,board):
        smallArray = board[:self.oneBoardSize, :self.oneBoardSize]

        B = np.reshape(smallArray, (1, self.oneBoardSize ** 2))
        for i in range(0, self.sc.GetSizeX()-self.oneBoardSize+1):
            for j in range(0, self.sc.GetSizeY()-self.oneBoardSize+1):
                if i != 0 or j != 0:
                    smallArray = board[i:i+self.oneBoardSize, j:j+self.oneBoardSize]
                    smallArray = np.reshape(smallArray, (1,self.oneBoardSize**2))
                    B = np.append(B, smallArray, axis=0)
        return B

saper = SaperController()
saper.createBoard(5, 7, 7)
print(saper.board)
player = Player(saper)
player.PrepareData()