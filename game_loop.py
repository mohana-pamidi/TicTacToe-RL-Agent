from tic_tac_toe import ticTacToe

if __name__ == '__main__':
    game = ticTacToe()
    print("Made game")
    game_over = False

    bot_token = 'o'
    player_token = 'x'

    print("Player is: x")
    print("bot is: o")

    print("bot is starting...")
    num_of_spots = 9

    while(not game_over):
          
        print("Bot's move: ")

        board_state = str(game.getBoard())

        row, col = game.get_RL_bot_move(board_state)

        game.placeToken(bot_token, row, col)
        num_of_spots-=1

        game.printBoard(game.getBoard())

        game_over = game.checkWinState(bot_token, row, col)

        if(game_over):
            print("Agent has won!")
            break

        else:

            print("\nEnter your move (row and column, 0-2):")

            row = int(input("Row (0-2): "))
            col = int(input("Column (0-2): "))

            game.placeToken(player_token, row, col)
            num_of_spots-=1

            game.printBoard(game.getBoard())

            game_over = game.checkWinState(player_token, row, col)

            if(game_over):
                print("Player has won!")
                break
            
        if(num_of_spots <= 0):

            game_over = True
            print("Draw!")


        

        
