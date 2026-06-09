from tic_tac_toe import ticTacToe
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


class Interface():
    def __init__(self):
        self.game = ticTacToe()
        self.status = "active"

    def game_state_to_dict(self):
        # gives back board state in dict so JSON is compatible.
        return {
            "board": self.game.getBoard(),
            "status": self.status
        }


current_game = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"message": "API STILL UP!"})


@app.route("/api/new-game", methods=['POST'])
def new_game():
    global current_game
    current_game = Interface()
    return jsonify(
        {
            "success": True,
            "message": "New game made!",
            "game": current_game.game_state_to_dict()
        }
    )


@app.route("/api/make-move", methods=['POST'])
def make_move():
    global current_game

    if current_game is None:
        return jsonify(
            {
                "success": False,
                "error": "No game started. Start a new one."
            }
        )

    if current_game.status != "active":
        return jsonify(
            {
                "success": False,
                "error": f"Game already over: {current_game.status}"
            }
        )

    data = request.get_json()
    row = data.get('row')
    col = data.get('col')

    success = current_game.game.placeToken('o', row, col)

    if not success:
        return jsonify(
            {
                "success": False,
                "error": "Invalid move."
            }
        )

    # Check if player won
    player_won = current_game.game.checkWinState('o', row, col)
    if player_won:
        current_game.status = "player_wins"
        return jsonify(
            {
                "success": True,
                "message": "Human player wins!",
                "game": current_game.game_state_to_dict()
            }
        )

    # Check for draw (no empty cells)
    board = current_game.game.getBoard()
    empty_cells = any(board[r][c] == 0 for r in range(3) for c in range(3))
    if not empty_cells:
        current_game.status = "draw"
        return jsonify(
            {
                "success": True,
                "message": "It's a draw!",
                "game": current_game.game_state_to_dict()
            }
        )

    # AI's turn
    bot_row, bot_col = current_game.game.get_RL_bot_move(str(current_game.game.getBoard()))
    if bot_row is None:
        current_game.status = "draw"
        return jsonify(
            {
                "success": True,
                "message": "It's a draw!",
                "game": current_game.game_state_to_dict()
            }
        )

    current_game.game.placeToken('x', bot_row, bot_col)

    ai_wins = current_game.game.checkWinState('x', bot_row, bot_col)
    if ai_wins:
        current_game.status = "AI_wins"
        return jsonify(
            {
                "success": True,
                "message": "Bot won!",
                "game": current_game.game_state_to_dict()
            }
        )

    return jsonify(
        {
            "success": True,
            "message": "Bot move successful!",
            "game": current_game.game_state_to_dict()
        }
    )


@app.route('/api/board', methods=['GET'])
def get_board():
    if current_game is None:
        return jsonify(
            {
                "success": False,
                "error": "No game started",
            }
        )

    return jsonify(
        {
            "success": True,
            "game": current_game.game_state_to_dict()
        }
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
