import numpy as np
import tic_tac_toe

q_table = {} #to hold Q-values for each action-state pair
agent_token = 'x'
player_token = 'o'


def get_board_state_str(board):
    #print(str(board))
    return str(board)

#fill up values in q-table with actions that are possible. 
#can either place an x or o 9 possible locations
def init_q_table(state): 

    #if the same boad configuration is not aldready seen before,
    if(state not in q_table):

        #then add it as a key in our dictionary
        #for this state, there are nine possible actions the agent can take
        #nine cells that the token can be placed in
        #this key value pair is a state-action pair(for alll nine actions in that state)
        q_table[state] = np.zeros(9)

def choose_action(state, epsilon):
    
    #eplison of the time exploration
    #1- epsilpon of the time exploitation

    #np is uniform probabiltiy distribution
    n = np.random.uniform(0, 1)

    if(n < epsilon):

        return np.random.randint(0,9)
    
    elif(n > epsilon):

        #getting action that allows q function to reach a max
        #gives back index of action with the max
        return np.argmax(q_table[state])

def action_to_coordinates(action):
    row = 0
    col = 0
    counter = 0

    for i in range(0, 3):
        for j in range(0, 3):

            if(counter == action):

                return row, col
            
            counter += 1
            col += 1

        row += 1
        col = 0

    return row, col

def update_q_vals(state, action, reward, next_state, alpha, gamma):
    if next_state not in q_table:
        init_q_table(next_state)

    #expected total future reward from taking a certain action in that particilar state
    #Gives best possible future value for that state 
    max_future_q = np.max(q_table[next_state])    

    #Bellman Equation/temporal difference learning
    q_table[state][action] = q_table[state][action] + alpha * (reward + gamma * max_future_q - q_table[state][action])

def train_agent(episodes, epsilon, alpha, gamma):
   
    np.random.seed(42)
    reward  = 0
    for episode in range (0, episodes):

        #new env for each board
        game = tic_tac_toe.ticTacToe() 
        board = game.getBoard()
        init_q_table(get_board_state_str(board))
        game_over = False

        while(not game_over):
            state = get_board_state_str(board)
            #print("Board State: ", state)

            action = choose_action(state, epsilon)
            #print("Chosen action: ", action)

            row, col = action_to_coordinates(action)
            print("Row: ", row, "Col: ", col)
            
            # if placing token was sucesful
            if(game.placeToken(agent_token, row, col)): 

                if(game.checkWinState(agent_token)):

                    reward = 1

                    game_over = True

                else:
                    game.opponent_move(player_token)

                    if(game.checkWinState(player_token)):

                        reward = -1

                        game_over = True

                    else:

                        reward = 0

            #state represented as a string of board config
            next_state = get_board_state_str(game.getBoard())

            update_q_vals(state, action, reward, next_state, alpha, gamma)

            print("State: ", state)
            print("Action: ", action)
            print("Reward: ", reward)
            print("next_state: ", next_state)

        print("Game OVER")
        print("Starting new episode....")


if __name__ == "__main__":
    train_agent(1000, 0.3, 0.5, 0.3)
            




            


