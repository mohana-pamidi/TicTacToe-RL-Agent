from tic_tac_toe import ticTacToe
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

class Interface():
    

    def __init__(self):
        self.game = ticTacToe()
        self.status = "active"

    def game_state_to_dict(self):

        #gives abck board state in dict so JSON is compatable. 

        return {
            "board" : self.game.getBoard(),
            "status" : self.status
        }
    
    current_game = None
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({"message" : "API STILL UP!"})

    @app.route("/api/new-game", methods=['POST'])
    def new_game():
        global current_game 

        #makes new game with new tic tac toe board
        current_game = Interface()

        return jsonify(
            {
                "success" : True,
                "message" : "New game made!",
                "game" : current_game.game_state_to_dict()
            }
        )
    
    @app.route("/api/make-move", methods=['POST'])
    def make_move():
        global current_game 

        #makes new game with new tic tac toe board
        if current_game is None:
        
            return jsonify(
                {
                    "success" : False,
                    "error" : "No game started. Start a new one."
                }
            )
        
        #get requested move from here
        data = request.get_json()
        row = data.get('row')
        col = data.get('col')

        success = current_game.game.placeToken('o', row, col)

        #if move was invalid
        if not success:
            return jsonify(
                {
                    "success" : False,
                    "error" : "Invalid move."
                }
            )
        
        #to chekc if player won since move could be invalid since the board is full
        player_won = current_game.game.checkWinState('o', row, col)

        if player_won:
            current_game.status = "player_wins"
            
            return jsonify(
                {
                    "success" : True,
                    "error" : "Human player wins!",
                    "game" : current_game.game_state_to_dict()
                }
            )
        
        #it is  AI's turn now
        bot_row, bot_col = current_game.game.get_RL_bot_move(str(current_game.game.getBoard()))
        current_game.game.placeToken('x', bot_row, bot_col)

        ai_wins = current_game.game.checkWinState('x', bot_row, bot_col)

        if ai_wins:
            current_game.status = "AI_wins"

            return jsonify(
                {
                    "success" : True,
                    "error" : "Bot won!",
                    "game" : current_game.game_state_to_dict()
                }
            )

        return jsonify(
                {
                    "success" : True,
                    "error" : "Bot move sucessful!",
                    "game" : current_game.game_state_to_dict()
                }
            ) 
    @app.route('/api/board', methods=['GET']) #We are getting board back to use it within our backend
    def get_board():

        if current_game is None:
            return jsonify(
                {
                    "success" : False,
                    "error" : "No game started",
                }
            ) 
        return jsonify(
            {
                "success" : True,
                "game" : current_game.game_state_to_dict()
            }
        ) 
        
if __name__ =='__main__':
    app.run(debug=True, port=5000)


        



        
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)



    



   

