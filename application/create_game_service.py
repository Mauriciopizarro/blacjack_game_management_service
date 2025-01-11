from domain.game import Game
from domain.exceptions import GameAlreadyCreated
from domain.interfaces.game_repository import GameRepository
from domain.player import Player


class CreateGameService:

    def __init__(self, game_repository: GameRepository):
        self.game_repository = game_repository

    def create_game(self, user_id: str, username: str):
        created_game = self.game_repository.has_created_game(user_id)
        if created_game:
            raise GameAlreadyCreated(created_game)
        admin = Player(name=username, user_id=user_id)
        game = Game(status="created", players=[admin], admin=admin)
        response_game = self.game_repository.save(game)
        return response_game
