import enum


class GameStatus(enum.Enum):
    Waiting = 1  # Game is still waiting for a second player to join
    NotOver = 2  # Game is active between two players
    PlayerOneUnderCheck = 3
    PlayerTwoUnderCheck = 4
    PlayerOneCheckmate = 5
    PlayerTwoCheckmate = 6
    PlayerOneWon = 7
    PlayerTwoWon = 8
    Stalemate = 9
