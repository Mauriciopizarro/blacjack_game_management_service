from domain.interfaces.game_repository import GameRepository
from domain.interfaces.publisher import Publisher
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig


dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class StartGameService:

    def __init__(
            self,
            game_repository: GameRepository,
            publisher: Publisher
    ):
        self.game_repository = game_repository
        self.publisher = publisher

    def start_game(self, game_id, user_id):
        game = self.game_repository.get(game_id)
        game.start(user_id)
        self.game_repository.update(game)
        self.publisher.send_message(message=game.dict(), topic="game_started")
        logger.info("Game started in management_service and message sent to game_service")
