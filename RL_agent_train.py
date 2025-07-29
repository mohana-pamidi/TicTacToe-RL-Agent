import numpy as np
import tic_tac_toe
import json
import sys
import matplotlib.pyplot as plt

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

def update_q_vals(state, action, reward, next_state, alpha, gamma):
    if next_state not in q_table:
        init_q_table(next_state)

    #expected total future reward from taking a certain action in that particilar state
    #Gives best possible future value for that state 
    max_future_q = np.max(q_table[next_state])    

    #Bellman Equation/temporal difference learning
    q_table[state][action] = q_table[state][action] + alpha * (reward + gamma * max_future_q - q_table[state][action])

def save_q_table(table):
    json_q_table = {}
    try:
        for state, values in q_table.items():
            json_q_table[state] = values.tolist()

        with open("q_table.json", 'w') as file:
            json.dump(json_q_table, file, indent=2)

        print("Q table sucessfully saved to \"q_table.json\"")

    except Exception:
        print(f"Error saving Q-table as JSON: {Exception}")




def train_agent(episodes, epsilon, alpha, gamma):
   
    np.random.seed(42)
    reward  = 0
    print("training starting...")
    rewards = []
    episodesNum = []

    # plt.plot(episodesNum, rewards, '-ro', label='Rewards vs Time', linewidth=2)
    # plt.show(block=True)
    
    for episode in range (0, episodes):

        #new env for each board
        game = tic_tac_toe.ticTacToe() 
        board = game.getBoard()
        init_q_table(get_board_state_str(board))
        game_over = False
        episode_reward = 0 
        
        if episode % 100 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()

        while(not game_over):
            state = get_board_state_str(board)
            #print("Board State: ", state)

            action = choose_action(state, epsilon)
            #print("Chosen action: ", action)

            row, col = game.action_to_coordinates(action)
            #print("Row: ", row, "Col: ", col)
            
            # if placing token was sucesful
            if(game.placeToken(agent_token, row, col)): 

                if(game.checkWinState(agent_token, row, col)):

                    reward = 1

                    game_over = True

                else:
                    placed, row, col = game.opponent_move(player_token)

                    if(placed):
                        if(game.checkWinState(player_token, row, col)):

                            reward = -1

                            game_over = True

                        else:

                            reward = 0

                    #if game is a draw, and cant place anymmore tokens      
                    else:
                        reward = 0

                        game_over = True
                        
            else: #invalid move so negative reward
                reward = -0.5

            #state represented as a string of board config
            next_state = get_board_state_str(game.getBoard())
            episode_reward += reward
            update_q_vals(state, action, reward, next_state, alpha, gamma)

            # print("State: ", state)
            # print("Action: ", action)
            # print("current_ state: ", next_state)
            # print("Reward: ", reward)


        rewards.append(episode_reward)
        episodesNum.append(episode)

        # print("Game OVER")
        # print("Starting new episode....")

    print("Finished Traning, saving q-table")
    
    save_q_table(q_table)

    plt.plot(episodesNum, rewards, label='Rewards vs Episode')

    plt.legend()

    print(plt.savefig("trainingPlot.png"))
    
    plt.show(block=True)


if __name__ == "__main__":

    train_agent(50000, 0.3, 0.5, 0.9)
            




            


