from typing import Tuple
from . import game
from .move import Move


class Player:
    def __init__(self, color: str):
        self.color = color
        self.total_games_played = 0
        self.white_side = False
        self.my_game: game.Game = None

    def is_checked(self):
        pass

    def select_piece(self, start_pos: Tuple[int, int]) -> Tuple[bool, str]:
        """
        This method lets user select a piece to move.

        :param start_pos: Tuple signifying the initial pos of the piece the
                          player is trying to move
        :return: boolean, True if selection valid; str determines the
                          failure reason.
        """

        return self.my_game.game_board.is_select_valid(start_pos, self)

    def make_move(self, start_pos: Tuple[int, int],
                  final_pos: Tuple[int, int]) -> None:
        """
        This method will be invoked by the user, to make a move.

        :param start_pos: Tuple signifying the initial pos of the piece the
                          player is trying to move
        :param final_pos: Tuple signifying the final pos of the piece the
                          player is trying to move
        :return: None
        """

        new_move = Move(start_pos, final_pos)
        new_move.move_player = self
        self.my_game.game_board.move_piece(new_move)
