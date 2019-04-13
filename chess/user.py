from typing import Dict
from chess.Game.game import Game
from chess.Game.player import Player
from uuid import UUID


class User:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password
        self.gamePlayers: Dict[UUID, Player] = {}

    def create_game(self) -> UUID:
        """
        Creates a new game for the user.

        :return: Game Id
        """

        new_game = Game()
        self.gamePlayers[new_game.id] = new_game.start_game()
        return new_game.id

    def join_game(self, game_id: UUID) -> bool:
        """
        Gets the game from the store and assigns player2 to this user.

        :param game_id: id for the game user wants to join
        :return: bool, True if successfully joined the game
        """

        pass