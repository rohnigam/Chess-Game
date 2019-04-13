from .piece import Piece
from .pieceType import PieceType


class Rook(Piece):
    def __init__(self, player, pos_x, pos_y):
        super().__init__(PieceType.Rook, player, pos_x, pos_y)

    def is_move_valid(self, final_x, final_y) -> bool:
        return True

    def draw_moves(self):
        return [None]


