from .piece import Piece
from .pieceType import PieceType


class Bishop(Piece):
    def __init__(self, player, pos_x, pos_y):
        super().__init__(PieceType.Bishop, player, pos_x, pos_y)

    def is_move_valid(self, final_x, final_y) -> bool:
        """
        Check if the move initiated is valid.
        A bishop moves in diagonals and cannot leap a piece.
        :param final_x: int signifying the final position of the piece being moved
        :param final_y: int signifying the final position of the piece being moved
        :return: boolean, True if move is valid
        """

        if abs(final_x - self.pos_x) == abs(final_y - self.pos_y):
            return self.is_leap_valid(final_x, final_y)

        return False

    def draw_moves(self):
        # not sure what its supposed to right now
        return []


