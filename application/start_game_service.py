from dependency_injector.wiring import Provide, inject
from domain.interfaces.game_repository import GameRepository
from infrastructure.injector import Injector
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig


dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class StartGameService:

    @inject
    def __init__(self, game_repository: GameRepository = Provide[Injector.game_management_repo]):
        self.game_repository = game_repository

    def start_game(self, game_id, user_id):
        game = self.game_repository.get(game_id)
        game.start(user_id)
        self.game_repository.update(game)
        #pub.sendMessage('game_started', event=game.dict())
        logger.warning("Please trigger an event from a message broker")
