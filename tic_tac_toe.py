import numpy as np
import random

class ticTacToe:


    def __init__(self):

        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


    def placeToken(self, token, row, col):

        if(self.board[row][col] == 0):

            self.board[row][col] = token

            return True
        
        else:

            return False
        
    def opponent_move(self, token):
        row = np.random.randint(0,3)
        col = np.random.randint(0,3)

        if(self.board[row][col] == 0):

            self.board[row][col] = token

            return True
        
        else:

            return False
    def getBoard(self):
        return self.board
    
    def checkWinState(self, token):

        x = [-1, -1, 0, 1, 1, 1, 0, -1]
        y = [ 0, 1, 1, 1, 0, -1, -1, -1]

        for i in range (0, 3):

            for j in range(0, 3):

                if(self.board[i][j] == token):

                    for k in range (0, len(x)):
                        
                        #checking if in bounds of game
                        if((i - y[k]) < 3 and (j - x[k]) < 3 and (i - (2 * y[k])) < 3 and (j - (2 * x[k])) < 3):

                            #cecking if next two slots are filled up disgaonally up, down, left or right
                            if((self.board[i - y[k]][j - x[k]] == token) and
                            (self.board[i - (2 * y[k])][j - (2 * x[k])] == token)):
                                
                                return True

        return False
    


