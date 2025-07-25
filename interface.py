from tic_tac_toe import ticTacToe
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

class interface():
    

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
    # @app.route('/api/health', methods=['GET'])
    # def health():
    #     return jsonify({"message" : "API STILL UP!"})

    @app.route("/")
    def index():
        return "Hello, World!"
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)



    



   

