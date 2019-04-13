from abc import ABC, abstractmethod
from .pieceType import PieceType


class Piece(ABC):
    def __init__(self, piece_type: PieceType, player, pos_x, pos_y):
        self.piece_type = piece_type
        self.player = player
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.captured = False

    @abstractmethod
    def is_move_valid(self, final_x, final_y) -> bool:
        pass

    def is_leap_valid(self, final_x, final_y) -> bool:
        """
        This method checks if the leap from start to final
        position valid. In general, most of the chess pieces
        cannot jump over a piece to get across.
        :param final_x: int
        :param final_y: int
        :return: boolean, True if leap is valid
        """

        # This will have a run complexity of O(n)
        return True

    @abstractmethod
    def draw_moves(self):
        pass

    def capture(self) -> None:
        self.captured = True

    def __str__(self):
        return '%s' % (str(self.piece_type).split('.')[1])
