import numpy as np
import random

class ticTacToe:


    def __init__(self):

        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.curr_col = 0
        self.curr_row = 0


    def placeToken(self, token, row, col):

        if(self.board[row][col] == 0):

            self.board[row][col] = token

            self.curr_row = row
            self.curr_col = col

            return True
        
        else:

            return False

    #this function only used for traning agent and will not be used for the actual game loop. 
    
    def opponent_move(self, token):

        attempts = 0; 
        max_attempts = 100

        while(attempts < max_attempts):

            row = np.random.randint(0,3)
            col = np.random.randint(0,3)

            if(self.board[row][col] == 0):

                self.board[row][col] = token

                return True, row, col
            
            attempts+=1

        return False, row, col
    
    def getBoard(self):
        return self.board

    
    def checkWinState(self, token, placedRow, placedCol):
        #just iterate the whole board
        # Just hceck from row and col of when toek was placed.
        counter = 0; 

        #checking sideways
        for col in range(0,3):
            if(self.board[placedRow][col] == token):
                counter+=1

        if(counter == 3):
            return True
        
        #checking up and down
        counter = 0; 

        for row in range(0,3):
            if(self.board[row][placedCol] == token):
                counter+=1

        if(counter == 3):
            return True

        #check left to right digonal
        counter = 0; 
        
        for i in range(0,3):
            if(self.board[i][i] == token):
                counter+=1

        if(counter == 3):
            return True 

        #check right to left digonal
        counter = 0; 
        
        for i in range(0,3):
            if(self.board[i][2-i] == token):
                counter+=1

        if(counter == 3):
            return True 


        return False
    


# if __name__ == '__main__':
#     game = ticTacToe()

#     print(game.checkWinState('x', 1, 0))

    


