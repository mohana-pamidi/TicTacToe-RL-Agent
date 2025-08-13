import numpy as np
import random
import json
import ast

class ticTacToe:

    def __init__(self):
        
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.curr_col = 0
        self.curr_row = 0

        with open("q_table.json") as json_file:
            self.q_table = json.load(json_file)

    def action_to_coordinates(self, action):

        board_action_Vals = {0 : [0,0], 1 : [0,1], 2 :[0, 2],
                            3 : [1,0], 4 : [1,1], 5 :[1, 2],
                            6 : [2,0], 7 : [2,1], 8 :[2, 2]}
        action_coords = board_action_Vals[action]

        #returns row and col
        return action_coords[0], action_coords[1]

    #this will be used to place token for both RL bot and human player

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
    
    def get_RL_bot_move(self, board_str):

        #cheks for open slots
        valid_actions = []
        for i in range(9):
            row, col = self.action_to_coordinates(i)
            if self.board[row][col] == 0: 
                valid_actions.append(i)

        try: 
            #get array of q_values for tha baord config so that you can modify and amke sure that the bot doesnt pick slots already taken up
            q_values = np.array(self.q_table[board_str]).copy()
                
            if not valid_actions:
                print("No valid moves available!")
                return None, None
            
            #if the action is invalid/alr a token in that slot, then make the q_val -infintiy
            for i in range(9):
                if i not in valid_actions:
                    q_values[i] = float('-inf')

            #get action with max q from the filtered q
            action = np.argmax(q_values)

        except:

            print("unforseen...Taking random action")
            action = np.random.choice(valid_actions)

        
        print("best bot action: " , action)
        row, col = self.action_to_coordinates(action)

       
        return row, col

    def getBoard(self):
        return self.board

    def printBoard(self, board):

        for row in board:
            print(" | ".join(str(cell) for cell in row))

        print("\n")

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

    


