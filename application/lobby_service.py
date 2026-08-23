from domain.interfaces.game_repository import GameRepository


class LobbyService:

    def __init__(self, game_repository: GameRepository):
        self.game_repository = game_repository

    def get_lobby(self, game_id: str) -> dict:
        game = self.game_repository.get(game_id)
        return {
            "game_id": game.id,
            "status": game.status,
            "admin": game.admin,
            "players": game.players
        }

    def get_lobby_list(self, user_id: str) -> dict:
        return {
            "user_id": user_id,
            "games": self.game_repository.get_games_by_user(user_id)
        }