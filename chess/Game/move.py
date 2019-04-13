from typing import Tuple
import chess.Pieces.piece as piece


class Move:
    def __init__(self, start_pos: Tuple[int, int],
                 final_pos: Tuple[int, int]):
        self.start_x = start_pos[0]
        self.start_y = start_pos[1]
        self.final_x = final_pos[0]
        self.final_y = final_pos[1]
        self.move_player = None
        self.piece: piece.Piece = None
        self.captured_piece: piece.Piece = None
