import numpy as np
import tic_tac_toe
import json
import matplotlib.pyplot as plt
from collections import defaultdict

class TicTacToeAgent:
    def __init__(self, q_table_file="q_table.json"):
        """Initialize the agent with a trained Q-table"""
        self.q_table = {}
        self.agent_token = 'x'
        self.player_token = 'o'
        self.load_q_table(q_table_file)
    
    def load_q_table(self, filename):
        """Load the trained Q-table from JSON file"""
        try:
            with open(filename, 'r') as file:
                json_q_table = json.load(file)
            
            # Convert back to numpy arrays
            for state, values in json_q_table.items():
                self.q_table[state] = np.array(values)
            
            print(f"Successfully loaded Q-table with {len(self.q_table)} states")
        except FileNotFoundError:
            print(f"Q-table file '{filename}' not found. Please train the model first.")
            return False
        except Exception as e:
            print(f"Error loading Q-table: {e}")
            return False
        return True
    
    def get_board_state_str(self, board):
        """Convert board to string representation"""
        return str(board)
    
    def get_best_action(self, state, game):
        """Get the best action based on Q-values for valid moves only"""
        if state not in self.q_table:
            # If state not in Q-table, choose random valid move
            valid_actions = []
            board = game.getBoard()
            for i in range(9):
                row, col = game.action_to_coordinates(i)
                if board[row][col] == 0:
                    valid_actions.append(i)
            return np.random.choice(valid_actions) if valid_actions else 0
        
        # Get Q-values for this state
        q_values = self.q_table[state].copy()
        
        # Set Q-values for invalid moves to negative infinity
        board = game.getBoard()
        for i in range(9):
            row, col = game.action_to_coordinates(i)
            if board[row][col] != 0:  # Invalid move
                q_values[i] = float('-inf')
        
        # Return action with highest Q-value
        return np.argmax(q_values)

class RandomOpponent:
    """Random opponent that makes random valid moves"""
    def __init__(self, token='o'):
        self.token = token
    
    def make_move(self, game):
        """Make a random valid move"""
        return game.opponent_move(self.token)

class OptimalOpponent:
    """Simple optimal opponent using minimax-like strategy"""
    def __init__(self, token='o'):
        self.token = token
        self.opponent_token = 'x'
    
    def make_move(self, game):
        """Make an optimal move using simple heuristics"""
        board = game.getBoard()
        
        # First, try to win
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    if game.placeToken(self.token, i, j):
                        if game.checkWinState(self.token, i, j):
                            return True, i, j
                        else:
                            # Undo the move
                            board[i][j] = 0
        
        # Second, try to block opponent from winning
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    if game.placeToken(self.opponent_token, i, j):
                        if game.checkWinState(self.opponent_token, i, j):
                            # Block this move
                            board[i][j] = 0
                            return game.placeToken(self.token, i, j), i, j
                        else:
                            # Undo the test move
                            board[i][j] = 0
        
        # Otherwise, make a random move
        return game.opponent_move(self.token)

def test_vs_opponent(agent, opponent, num_games=1000, verbose=False):
    """Test the agent against an opponent"""
    results = {'wins': 0, 'losses': 0, 'draws': 0}
    
    for game_num in range(num_games):
        game = tic_tac_toe.ticTacToe()
        game_over = False
        
        if verbose and game_num < 5:
            print(f"\n--- Game {game_num + 1} ---")
        
        while not game_over:
            # Agent's turn
            state = agent.get_board_state_str(game.getBoard())
            action = agent.get_best_action(state, game)
            row, col = game.action_to_coordinates(action)
            
            if game.placeToken(agent.agent_token, row, col):
                if verbose and game_num < 5:
                    print(f"Agent plays at ({row}, {col})")
                    game.printBoard(game.getBoard())
                
                if game.checkWinState(agent.agent_token, row, col):
                    results['wins'] += 1
                    if verbose and game_num < 5:
                        print("Agent wins!")
                    break
                
                # Opponent's turn
                if isinstance(opponent, RandomOpponent):
                    placed, opp_row, opp_col = opponent.make_move(game)
                else:
                    placed, opp_row, opp_col = opponent.make_move(game)
                
                if placed:
                    if verbose and game_num < 5:
                        print(f"Opponent plays at ({opp_row}, {opp_col})")
                        game.printBoard(game.getBoard())
                    
                    if game.checkWinState(opponent.token, opp_row, opp_col):
                        results['losses'] += 1
                        if verbose and game_num < 5:
                            print("Opponent wins!")
                        break
                else:
                    # Draw
                    results['draws'] += 1
                    if verbose and game_num < 5:
                        print("Draw!")
                    break
            else:
                # Invalid move by agent (shouldn't happen with proper implementation)
                if verbose:
                    print("Agent made invalid move!")
                break
    
    return results

def analyze_q_values(agent):
    """Analyze the Q-table to understand what the agent learned"""
    print(f"\nQ-Table Analysis:")
    print(f"Total states learned: {len(agent.q_table)}")
    
    # Find states with highest and lowest Q-values
    max_q_value = float('-inf')
    min_q_value = float('inf')
    max_state = None
    min_state = None
    
    for state, q_values in agent.q_table.items():
        max_q = np.max(q_values)
        min_q = np.min(q_values)
        
        if max_q > max_q_value:
            max_q_value = max_q
            max_state = state
        
        if min_q < min_q_value:
            min_q_value = min_q
            min_state = state
    
    print(f"Highest Q-value: {max_q_value:.3f}")
    print(f"Lowest Q-value: {min_q_value:.3f}")
    
    # Sample a few states and their Q-values
    print(f"\nSample Q-values for different states:")
    sample_states = list(agent.q_table.keys())[:5]
    for state in sample_states:
        print(f"State: {state}")
        print(f"Q-values: {agent.q_table[state]}")
        print()

def run_comprehensive_test():
    """Run comprehensive testing of the trained agent"""
    print("Loading trained agent...")
    agent = TicTacToeAgent()
    
    if not agent.q_table:
        print("No Q-table loaded. Please train the model first.")
        return
    
    # Analyze Q-values
    analyze_q_values(agent)
    
    print("\n" + "="*50)
    print("TESTING AGAINST RANDOM OPPONENT")
    print("="*50)
    
    random_opponent = RandomOpponent()
    random_results = test_vs_opponent(agent, random_opponent, num_games=1000, verbose=True)
    
    print(f"\nResults vs Random Opponent (1000 games):")
    print(f"Wins: {random_results['wins']} ({random_results['wins']/10:.1f}%)")
    print(f"Losses: {random_results['losses']} ({random_results['losses']/10:.1f}%)")
    print(f"Draws: {random_results['draws']} ({random_results['draws']/10:.1f}%)")
    
    print("\n" + "="*50)
    print("TESTING AGAINST OPTIMAL OPPONENT")
    print("="*50)
    
    optimal_opponent = OptimalOpponent()
    optimal_results = test_vs_opponent(agent, optimal_opponent, num_games=1000)
    
    print(f"\nResults vs Optimal Opponent (1000 games):")
    print(f"Wins: {optimal_results['wins']} ({optimal_results['wins']/10:.1f}%)")
    print(f"Losses: {optimal_results['losses']} ({optimal_results['losses']/10:.1f}%)")
    print(f"Draws: {optimal_results['draws']} ({optimal_results['draws']/10:.1f}%)")
    
    # Test with different numbers of games
    print("\n" + "="*50)
    print("PERFORMANCE ACROSS DIFFERENT GAME COUNTS")
    print("="*50)
    
    game_counts = [100, 500, 1000, 2000]
    random_win_rates = []
    optimal_win_rates = []
    
    for count in game_counts:
        # Test vs random
        random_res = test_vs_opponent(agent, random_opponent, num_games=count)
        random_win_rate = random_res['wins'] / count * 100
        random_win_rates.append(random_win_rate)
        
        # Test vs optimal
        optimal_res = test_vs_opponent(agent, optimal_opponent, num_games=count)
        optimal_win_rate = optimal_res['wins'] / count * 100
        optimal_win_rates.append(optimal_win_rate)
        
        print(f"{count} games - Random: {random_win_rate:.1f}% wins, Optimal: {optimal_win_rate:.1f}% wins")
    
    # Plot results
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.bar(['Wins', 'Losses', 'Draws'], 
            [random_results['wins'], random_results['losses'], random_results['draws']],
            color=['green', 'red', 'gray'])
    plt.title('vs Random Opponent (1000 games)')
    plt.ylabel('Number of games')
    
    plt.subplot(1, 2, 2)
    plt.bar(['Wins', 'Losses', 'Draws'], 
            [optimal_results['wins'], optimal_results['losses'], optimal_results['draws']],
            color=['green', 'red', 'gray'])
    plt.title('vs Optimal Opponent (1000 games)')
    plt.ylabel('Number of games')
    
    plt.tight_layout()
    plt.savefig('test_results.png')
    plt.show()
    
    # Win rate trend
    plt.figure(figsize=(10, 6))
    plt.plot(game_counts, random_win_rates, 'b-o', label='vs Random', linewidth=2, markersize=8)
    plt.plot(game_counts, optimal_win_rates, 'r-s', label='vs Optimal', linewidth=2, markersize=8)
    plt.xlabel('Number of Games')
    plt.ylabel('Win Rate (%)')
    plt.title('Agent Win Rate vs Different Opponents')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('win_rate_trend.png')
    plt.show()
    
    print(f"\nTest results saved as 'test_results.png' and 'win_rate_trend.png'")

def interactive_test():
    """Allow user to play against the trained agent"""
    print("Loading trained agent for interactive play...")
    agent = TicTacToeAgent()
    
    if not agent.q_table:
        print("No Q-table loaded. Please train the model first.")
        return
    
    print("\n" + "="*50)
    print("PLAY AGAINST THE TRAINED AGENT")
    print("="*50)
    print("You are 'O', Agent is 'X'")
    print("Enter moves as row,col (0-2 for each)")
    print("Type 'quit' to exit")
    
    while True:
        game = tic_tac_toe.ticTacToe()
        game_over = False
        
        print("\nNew game started!")
        game.printBoard(game.getBoard())
        
        while not game_over:
            # Agent's turn (X)
            state = agent.get_board_state_str(game.getBoard())
            action = agent.get_best_action(state, game)
            row, col = game.action_to_coordinates(action)
            
            if game.placeToken('x', row, col):
                print(f"\nAgent plays X at ({row}, {col})")
                game.printBoard(game.getBoard())
                
                if game.checkWinState('x', row, col):
                    print("Agent wins!")
                    break
                
                # Check if board is full
                board = game.getBoard()
                if all(board[i][j] != 0 for i in range(3) for j in range(3)):
                    print("It's a draw!")
                    break
                
                # Human's turn (O)
                while True:
                    try:
                        move = input("\nYour move (row,col) or 'quit': ").strip()
                        if move.lower() == 'quit':
                            return
                        
                        human_row, human_col = map(int, move.split(','))
                        if 0 <= human_row <= 2 and 0 <= human_col <= 2:
                            if game.placeToken('o', human_row, human_col):
                                print(f"You play O at ({human_row}, {human_col})")
                                game.printBoard(game.getBoard())
                                
                                if game.checkWinState('o', human_row, human_col):
                                    print("You win!")
                                    game_over = True
                                break
                            else:
                                print("Invalid move! That position is already taken.")
                        else:
                            print("Invalid input! Use row,col with values 0-2.")
                    except:
                        print("Invalid input! Use format: row,col (e.g., 1,2)")
        
        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again != 'y':
            break

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_test()
    else:
        run_comprehensive_test()
        
        # Ask if user wants to play interactively
        play = input("\nWould you like to play against the agent? (y/n): ").strip().lower()
        if play == 'y':
            interactive_test()
