import numpy as np
from Saper.SaperController import SaperController

class Player:
    def __init__(self, saperController):
        self.sc=saperController
        board = saperController.GetBoard()
        """board = np.array([[ 0,  1,  1,  1,  1, -1,  1],
                         [ 0 , 1 ,-1 , 1 , 1 , 1 , 1],
                         [ 0 , 1  ,1  ,1,  0  ,0,  0],
                         [ 0  ,0  ,0  ,0 , 1  ,1,  1],
                         [ 0  ,0 , 0  ,1 , 2 ,-1 , 1],
                         [ 1  ,1 , 0 , 1 ,-1 , 2 , 1],
                         [-1  ,1,  0  ,1  ,1,  1 , 0]])"""
        self.oneBoardSize = 4
        self.hiddenLayerSize = 50

        smallArray = board[:self.oneBoardSize, :self.oneBoardSize]
        print(smallArray)
        self.X = np.reshape(smallArray, (1, self.oneBoardSize ** 2))

        for i in range(0, 7-self.oneBoardSize+1): #self.sc.GetSizeX()
            for j in range(0, 7-self.oneBoardSize+1): #self.sc.GetSizeY()
                if i != 0 or j != 0:
                    smallArray = board[i:i+self.oneBoardSize, j:j+self.oneBoardSize]
                    #print("SA:" )
                    #print(smallArray)
                    smallArray = np.reshape(smallArray, (1,self.oneBoardSize**2))
                    self.X = np.append(self.X, smallArray, axis=0)
                    #print("X:" )
                    #print(self.X)

        self.params = {}
        self.params['W1'] = np.random.randn(self.oneBoardSize**2, self.hiddenLayerSize) * 0.001
        self.params['b1'] = np.zeros(self.hiddenLayerSize)
        self.params['W2'] = np.random.randn(self.hiddenLayerSize, self.oneBoardSize**2) * 0.001
        self.params['b2'] = np.zeros(self.oneBoardSize**2)


saper = SaperController()
saper.createBoard(5, 7, 7)
player = Player(saper)