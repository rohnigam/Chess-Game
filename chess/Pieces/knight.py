from .piece import Piece
from .pieceType import PieceType


class Knight(Piece):
    def __init__(self, player, pos_x, pos_y):
        super().__init__(PieceType.Knight, player, pos_x, pos_y)

    def is_move_valid(self, final_x, final_y) -> bool:

        if abs(self.pos_y - final_y) > 0 and \
            abs(self.pos_x - final_x) > 0 and \
            abs(self.pos_y - final_y) + abs(self.pos_x - final_x) == 3:

            return True

        return False

    def is_leap_valid(self, final_x, final_y) -> bool:
        """
        For a knight, any leap is valid.
        :param final_x: int
        :param final_y: int
        :return: True
        """
        return True

    def draw_moves(self):
        return [None]


