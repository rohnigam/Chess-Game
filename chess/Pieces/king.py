from .piece import Piece
from .pieceType import PieceType


class King(Piece):
    def __init__(self, player, pos_x, pos_y):
        super().__init__(PieceType.King, player, pos_x, pos_y)

    def is_move_valid(self, final_x, final_y):
        # Bishop moves in Diagonals
        # hence, a valid move
        return True

    def draw_moves(self):
        return [None]


