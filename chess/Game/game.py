from .player import Player
from .gameBoard import GameBoard
from .gameStatus import GameStatus
import uuid


class Game:
    def __init__(self):
        self.id = uuid.uuid4()
        self.player1: Player = None
        self.player2: Player = None
        self.game_board: GameBoard = None
        self.winner: Player = None

    def start_game(self) -> Player:
        """
        This method would setup a Game.
        The game starts when a second player joins the game.

        :return: Player object for this user
        """

        self.player1 = Player('red')
        self.player2 = Player('blue')
        self.player1.my_game = self
        self.player2.my_game = self
        self.game_board = GameBoard(8, self.player1, self.player2)

        return self.player1

    def join_game(self) -> Player:
        """
        This method will be used a user to join an already created game.

        :return: Player
        """

        self.game_board.game_status = GameStatus.NotOver
        return self.player2

    def check_game_status(self) -> GameStatus:
        """
        This api checks and returns the status of the game.

        :return: GameStatus
        """

        return self.game_board.game_status

    def result(self) -> str:
        """
        Returns the result of the match in string format.

        :return: str
        """

        if self.check_game_status() == GameStatus.PlayerOneWon:
            return 'Player1 Wins !'
        elif self.check_game_status() == GameStatus.PlayerTwoWon:
            return 'Player2 Wins !'
        elif self.check_game_status() == GameStatus.Stalemate:
            return 'Stalemate :('

    def game_over(self) -> bool:
        """
        This api returns true if game is over.
        Game is over when one player wins or if there is a stalemate.

        :return: bool, True if game over
        """

        status = self.check_game_status()
        if status == GameStatus.PlayerOneWon or status == GameStatus.PlayerTwoWon or status == GameStatus.Stalemate:
            return True

        return False
