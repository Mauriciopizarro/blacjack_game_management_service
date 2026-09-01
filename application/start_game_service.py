from domain.interfaces.game_repository import GameRepository
from infrastructure.http_clients.game_service_http_client import GameServiceHttpClient
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig


dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class StartGameService:

    def __init__(
            self,
            game_repository: GameRepository,
            game_service_http_client: GameServiceHttpClient
    ):
        self.game_repository = game_repository
        self.game_service_http_client = game_service_http_client

    def start_game(self, game_id, user_id):
        game = self.game_repository.get(game_id)
        game.start(user_id)
        self.game_repository.update(game)
        self.game_service_http_client.create_game(game_id=game.id, players=game.players)
        logger.info("Game started in management_service and game created in game_service via HTTP")
