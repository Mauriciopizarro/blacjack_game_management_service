import requests
from config import settings
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class GameServiceHttpClient:

    create_game_path = "/game/create"

    def create_game(self, game_id: str, players):
        """Sends the created game to the game_service via HTTP."""
        url = f"{settings.GAME_SERVICE_URL}{self.create_game_path}"
        response = requests.post(url=url, json={
            "game_id": game_id,
            "players": [
                {"name": player.name, "user_id": player.user_id} for player in players
            ]
        })
        response.raise_for_status()
        logger.info("Game created in game_service via HTTP")