from typing import List, Union, Tuple
from termcolor import colored
from .player import Player
from .move import Move
from chess.Pieces.piece import Piece
from chess.Pieces.bishop import Bishop
from chess.Pieces.pawn import Pawn
from chess.Pieces.king import King
from chess.Pieces.queen import Queen
from chess.Pieces.rook import Rook
from chess.Pieces.knight import Knight
from chess.Game.GameExceptions.invalidMove import InvalidMoveError
from chess.Game.gameStatus import GameStatus


class GameBoard:

    def __init__(self, board_size: int, player1: Player, player2: Player):
        self.board_size = board_size

        ''' Board saves the pieces, if no piece, value = None '''
        self.board: List[List[Union[Piece, None]]] = [[None]*self.board_size for _ in range(self.board_size)]
        self.player1 = player1
        self.player2 = player2

        self.moves_list: List[Move] = []
        self.game_status: GameStatus = GameStatus.Waiting

        self.player_turn = self.player1 # TO-DO: Need to randomize who goes first

        # Set the pieces on their initial position for player1 and player2
        self.set_pieces()

    def set_pieces(self) -> None:
        """
        Sets pieces on the board for both players.
        We are visualizing the board vertically, with player1
        starting from the top most rows and player2 starting from
        the bottommost rows.
        :return: void
        """

        self.set_player1_pieces()
        self.set_player2_pieces()

    def set_player1_pieces(self) -> None:
        """
        Set player1 pieces.

        :return: void
        """

        self.board[0][0], self.board[0][7] = Rook(self.player1, 0, 0), Rook(self.player1, 7, 0)
        self.board[0][1], self.board[0][6] = Knight(self.player1, 1, 0), Knight(self.player1, 6, 0)
        self.board[0][2], self.board[0][5] = Bishop(self.player1, 3, 0), Bishop(self.player1, 5, 0)
        self.board[0][4] = Queen(self.player1, 4, 0)
        self.board[0][3] = King(self.player1, 3, 0)
        self.board[1] = [Pawn(self.player1, x_pos, 1) for x_pos in range(8)]

    def set_player2_pieces(self) -> None:
        """
        Set player 2 pieces

        :return: void
        """

        self.board[7][0], self.board[7][7] = Rook(self.player2, 0, 7), Rook(self.player2, 7, 7)
        self.board[7][1], self.board[7][6] = Knight(self.player2, 1, 7), Knight(self.player2, 6, 7)
        self.board[7][2], self.board[7][5] = Bishop(self.player2, 2, 7), Bishop(self.player2, 5, 7)
        self.board[7][4] = Queen(self.player2, 4, 7)
        self.board[7][3] = King(self.player2, 3, 7)
        self.board[6] = [Pawn(self.player2, x_pos, 6) for x_pos in range(8)]

    def move_piece(self, new_move: Move) -> None:
        """
        This method makes the move of the piece at start_pos to
        final_pos on the board, if its a valid move

        :param new_move: Move initiated by a player
        :return: None
        :throws: InvalidMoveError exception if the move made is invalid.
        """

        start_pos = new_move.start_x, new_move.start_y
        final_pos = new_move.final_x, new_move.final_y
        valid_move, invalid_reason = self.is_move_valid(new_move)
        if valid_move:
            moving_piece = self.board[start_pos[1]][start_pos[0]]
            captured_piece = self.board[final_pos[1]][final_pos[0]]
            if captured_piece:
                captured_piece.capture()

            new_move.piece = moving_piece
            new_move.captured_piece = captured_piece
            self.save_move(new_move)

            moving_piece.pos_x = final_pos[0]
            moving_piece.pos_y = final_pos[1]

            self.board[final_pos[1]][final_pos[0]] = moving_piece
            self.board[start_pos[1]][start_pos[0]] = None

            self.toggle_player_turn()

            self.update_game_status()

        else:
            raise InvalidMoveError(invalid_reason)

    def is_select_valid(self, start_pos: Tuple[int, int],
                        move_player: Player) -> Tuple[bool, str]:
        """
        This validates whether the player can select
        to move piece at this position.
        Returns a bool and an error string

        :param start_pos:   Tuple signifying the initial pos of the piece the
                            player is trying to move
        :param move_player: Player that has initiated the move.
        :return: Tuple of bool and str, True if valid
        """

        if move_player != self.player_turn:
            return False, 'Move out of turn '

        if not self.is_within_bounds(start_pos):
            return False, 'Invalid Selection'

        if not self.board[start_pos[1]][start_pos[0]]:
            return False, 'Please select a valid piece to move'

        selected_piece = self.board[start_pos[1]][start_pos[0]]
        print('Selected Piece = %s'%selected_piece)

        if selected_piece.player != self.player_turn:
            return False, 'Cannot move piece of other player'

        return True, 'Success'

    def is_move_valid(self, new_move: Move) -> Tuple[bool, str]:
        """
        This api checks if a move initiated is valid or not and returns
        a boolean result along with an error string, describing the reason
        why the move is invalid.

        :param new_move: Move initiated by a player.
        :return: Tuple of bool and string.
        """

        start_pos = (new_move.start_x, new_move.start_y)
        final_pos = (new_move.final_x, new_move.final_y)
        valid_select, invalid_reason = self.is_select_valid(start_pos, new_move.move_player)
        if not valid_select:
            return False, invalid_reason

        moving_piece = self.board[start_pos[1]][start_pos[0]]

        if not moving_piece.is_move_valid(final_pos[0], final_pos[1]):
            return False, 'Invalid Move for Piece'

        valid_final_pos, invalid_reason = self.is_final_pos_valid(moving_piece, final_pos)
        if not valid_final_pos:
            return False, invalid_reason

        return True, 'Success'

    def is_final_pos_valid(self, moving_piece: Piece,
                           final_pos: Tuple[int, int]) -> Tuple[bool, str]:
        """
        This method validates if the final pos initiated in a move is valid.

        :param moving_piece: the moving piece
        :param final_pos: Tuple signifying the final pos of the piece the
                          player is trying to move
        :return: Tuple of bool(True if valid) and string(reason if move pos invalid)
        """
        if not self.is_within_bounds(final_pos):
            return False, 'Invalid Final Position'

        if self.board[final_pos[1]][final_pos[0]]:
            # if the final position contains a piece,
            # make sure its not of the same player.
            if moving_piece.player == self.board[final_pos[1]][final_pos[0]].player:
                return False, 'Cannot make a move on your own player'

        return True, 'Success'

    def is_within_bounds(self, position: Tuple[int, int]) -> bool:
        """
        Checks whether a position (x, y)
        is a valid position on the board.

        :param position: Tuple signifying the final pos of the piece the
                         player is trying to move
        :return: boolean, True if position is within bounds
        """

        if 0 <= position[0] < self.board_size and 0 <= position[1] < self.board_size:
            return True

        return False

    def save_move(self, new_move: Move) -> None:
        """
        Creates a move and appends it to the movesList.

        :param new_move: Move to be saved
        :return: void
        """

        self.moves_list.append(new_move)

    def toggle_player_turn(self) -> None:
        """
        This api toggles the playerTurn to the other player after a
        successful move.

        :return: void
        """

        if self.player_turn == self.player1:
            self.player_turn = self.player2
        else:
            self.player_turn = self.player1

    def update_game_status(self) -> None:
        """
        This api updates the game status based on the latest made move.

        :return: None
        """

        if not self.moves_list:
            # no move, no update in game status
            return

        latest_move = self.moves_list[-1]

        if self.has_player_won(latest_move):
            if latest_move.move_player == self.player1:
                self.game_status = GameStatus.PlayerOneWon
            else:
                self.game_status = GameStatus.PlayerTwoWon
        elif self.is_player1_under_checkmate():
            self.game_status = GameStatus.PlayerOneCheckmate
        elif self.is_player2_under_checkmate():
            self.game_status = GameStatus.PlayerTwoCheckmate
        elif self.is_player1_under_check():
            self.game_status = GameStatus.PlayerOneUnderCheck
        elif self.is_player2_under_check():
            self.game_status = GameStatus.PlayerTwoUnderCheck
        elif self.is_game_under_stalemate():
            self.game_status = GameStatus.Stalemate

    def has_player_won(self, latest_move: Move) -> bool:
        return False

    def is_player1_under_checkmate(self) -> bool:
        return False

    def is_player2_under_checkmate(self) -> bool:
        return False

    def is_player1_under_check(self) -> bool:
        return False

    def is_player2_under_check(self) -> bool:
        return False

    def is_game_under_stalemate(self) -> bool:
        return False

    def check_game_status(self) -> GameStatus:
        """
        This api returns the game status at the current moment.

        :return: GameStatus
        """

        return self.game_status

    def __str__(self):
        board_str = colored('%45s\n'%'Player 1', self.player1.color)
        for row in self.board:
            for spot in row:
                if spot:
                    board_str += colored('%10s'%spot, spot.player.color)
                else:
                    board_str += ' ' * 10
            board_str += '\n'

        board_str += colored('%45s' % 'Player 2', self.player2.color)

        return board_str


