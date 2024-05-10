from domain.game import Game
from domain.exceptions import GameAlreadyCreated
from domain.interfaces.game_repository import GameRepository
from domain.player import Player
from dependency_injector.wiring import Provide, inject
from infrastructure.injector import Injector


class CreateGameService:

    @inject
    def __init__(self, game_repository: GameRepository = Provide[Injector.game_management_repo]):
        self.game_repository = game_repository

    def create_game(self, user_id: str, username: str):
        if self.game_repository.has_created_game(user_id):
            game_created = self.game_repository.get_created_game()
            raise GameAlreadyCreated(game_created.id)
        admin = Player(name=username, user_id=user_id)
        game = Game(status="created", players=[admin], admin=admin)
        response_game = self.game_repository.save(game)
        return response_game
