import enum


class MoveResult(enum.Enum):

    Invalid = 1
    Valid = 2
    CheckMate = 3
    Stalemate = 4
