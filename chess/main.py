from chess.Game.game import Game
from chess.Game.gameStatus import GameStatus
from chess.Game.GameExceptions.invalidMove import InvalidMoveError


def main():
    new_game = Game()
    player1 = new_game.start_game()
    player2 = new_game.join_game()
    print(new_game.game_board)

    while new_game.check_game_status() == GameStatus.NotOver:
        choice = int(input('Enter 1 for player1 and 2 for player 2 to make a move  '))
        if choice == 1:
            current_player = player1
        elif choice == 2:
            current_player = player2
        else:
            print('Invalid choice')
            continue

        start_x, start_y, final_x, final_y = [int(x) for x in input('Enter move ').split()]

        try:
            current_player.make_move((start_x, start_y), (final_x, final_y))
        except InvalidMoveError as error:
            print(error)
            print('Try Again\n')
        else:
            # if move successful print the game status and game board
            print(new_game.check_game_status())
            print(new_game.game_board)

    print('Game Over !')
    print(new_game.result())


if __name__ == '__main__':
    main()
