import numpy as np
import random as rand

class Player:
    def __init__(self, app):
        self.sc = app.saper
        self.gui = app.gui
        self.oneBoardSize = 3
        self.hiddenLayerSize = 20

        self.W1 = np.random.randn(self.oneBoardSize**2, self.hiddenLayerSize) * 0.001
        self.b1 = np.zeros(self.hiddenLayerSize)
        self.W2 = np.random.randn(self.hiddenLayerSize, self.oneBoardSize**2) * 0.001
        self.b2 = np.zeros(self.oneBoardSize**2)


    def PrepareData(self):
        board = self.sc.GetBoard()
        board = np.array(board)

        self.X = self.reshape(board)

        self.y = np.array(self.sc.GetBoard())

        for i in range(0, self.sc.GetSizeX()):
            for j in range(0, self.sc.GetSizeY()):
                self.y[i,j] = int (self.sc.GetValueAt(i,j) == -1)

        self.y = self.reshape(self.y)


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

    def loss(self, X, y=None, reg=0.0):
        W1, b1 = self.W1, self.b1
        W2, b2 = self.W2, self.b2
        N, D = X.shape

        scores1 = np.maximum(0, X.dot(W1) + b1)
        scores2 = scores1.dot(W2) + b2
        scores = scores2
        num_train = X.shape[0]

        scores = scores[np.arange(num_train)] - np.max(scores[np.arange(num_train)])
        exp_scores = np.exp(scores)

        probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        corect_logprobs = -np.log(probs[np.transpose([np.arange(num_train)]), y])
        data_loss = np.sum(corect_logprobs) / num_train
        reg_loss = reg * np.sum(W1 * W1) + reg * np.sum(W2 * W2)
        loss = data_loss + reg_loss

        grads = {}
        dX2 = probs
        dX2[np.transpose([np.arange(num_train)]), y] -= 1

        dW2 = ((dX2.T).dot(scores1)).T / N + reg * W2
        db2 = (dX2.T).dot(np.ones(scores1.shape[0])) / num_train
        dX1 = dX2.dot(W2.T)
        dW1 = (((dX1 * (scores1 > 0)).T).dot(X)).T / N + reg * W1
        db1 = (((dX1 * (scores1 > 0)).T).dot(np.ones(X.shape[0]))).T / num_train

        grads['W2'] = dW2
        grads['b2'] = db2
        grads['W1'] = dW1
        grads['b1'] = db1

        return loss, grads

    def train(self,
              learning_rate=1e-3,
              reg=5e-6, num_iters=100, verbose=False):
        # num_train = self.X.shape[0]
        # iterations_per_epoch = max(num_train / batch_size, 1)

        loss_history = []
        train_acc_history = []
        win = 0
        lost = 0
        for i in range(0, num_iters):
            iteration = 0
            bombs = rand.randint(5, 10)
            width = rand.randint(10, 15)
            height = rand.randint(10, 15)
            self.sc.createBoard(bombs, width, height)
            self.sc.UncoverField(0, 0)
            self.gui.update_info(
                "Method: Neural Network\nGame:" + str(i+1) + "\nWin count:" + str(win) + "\nLost count:" + str(lost))
            self.gui.loadNewBoard()
            self.gui.refresh()
            while self.sc.GetState() == 0:

                self.PrepareData()
                loss, grads = self.loss(self.X, y=self.y, reg=reg)
                loss_history.append(loss)

                self.W1 -= learning_rate * grads['W1']
                self.b1 -= learning_rate * grads['b1']
                self.W2 -= learning_rate * grads['W2']
                self.b2 -= learning_rate * grads['b2']

                if verbose and i % 10 == 0:
                    print('iteration %d (%d. game): loss %f' % (iteration, i, loss))

                iteration += 1
                x = rand.randint(0, self.sc.GetSizeX() - 1)
                y = rand.randint(0, self.sc.GetSizeY() - 1)
                while (self.sc.GetBoard())[x][y] != 10:
                    x = rand.randint(0, self.sc.GetSizeX() - 1)
                    y = rand.randint(0, self.sc.GetSizeY() - 1)

                self.sc.UncoverField(x, y)

            if self.sc.GetState() == 1:
                win +=1
            if self.sc.GetState() == -1:
                lost +=1
            if verbose and i % 10 == 0 and i>100:
                tryGames = 10
                acc = self.checkAccuracy(tryGames)
                print(
                        'Moves %d (%d. game), accuracy in %d games: %f' % (
                        iteration, i, tryGames, acc))
            #if verbose:
            #    print('state: %d' % (self.sc.GetState()))

            self.gui.update_info(
                    "Method: Neural Network\nGame:" + str(i+1) + "\nWin count:" + str(win) + "\nLost count:" + str(lost))
            self.gui.refresh()

        return {
            'loss_history': loss_history,
            'train_acc_history': train_acc_history,
            #'val_acc_history': val_acc_history,
        }

    #niezrobiona do końca metoda
    def predict(self, X):
        num_train = X.shape[0]
        W1, b1 = self.W1, self.b1
        W2, b2 = self.W2, self.b2
        scores_t = np.maximum(0, X.dot(W1) + b1)
        scores = scores_t.dot(W2) + b2
        scores = scores[np.arange(num_train)] - np.max(scores[np.arange(num_train)])
        exp_scores = np.exp(scores)
        probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)

        pred_bombs = [[0 for y in range(self.sc.GetSizeY())] for x in range(self.sc.GetSizeX())]
        pred_bombs = np.array(pred_bombs)
        smallArSize = self.oneBoardSize
        size_y = self.sc.GetSizeY()
        size_x = self.sc.GetSizeX()
        for i in range(0, probs.shape[0]):
            for k in range(0, probs.shape[1]):
                a = int((int(i/(size_y - smallArSize + 1))+int(k/smallArSize))/size_y)
                b = (i%(size_y - smallArSize+1)+k%smallArSize)%size_y
                pred_bombs[a][b] = max(pred_bombs[a][b], probs[i][k])


        return pred_bombs

    def checkAccuracy(self, tries):
        win = 0
        for i in range(tries):
            bombs = rand.randint(4, 6)
            width = rand.randint(4, 6)
            self.sc.createBoard(bombs, width, width)
            self.sc.UncoverField(0, 0)

            while self.sc.GetState() == 0:

                self.PrepareData()
                pred_bombs = self.predict(self.X)
                x=int(np.argmin(pred_bombs)/self.sc.GetSizeY())
                y=np.argmin(pred_bombs)%self.sc.GetSizeY()
                while (self.sc.GetBoard())[x][y] != 10:
                    pred_bombs[x][y]=1
                    x=int(np.argmin(pred_bombs)/self.sc.GetSizeY())
                    y=np.argmin(pred_bombs)%self.sc.GetSizeY()

                self.sc.UncoverField(x, y)

            if self.sc.GetState() == 1:
                win +=1
                print("win")

        return win/tries

"""saper = SaperController()
saper.createBoard(5, 7, 7)
player = Player(saper)
player.train(num_iters=1000,verbose=True)"""