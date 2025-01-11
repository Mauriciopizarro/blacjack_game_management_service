from domain.interfaces.game_repository import GameRepository
from domain.player import Player


class EnrollPlayerService:

    def __init__(self, game_repository: GameRepository):
        self.game_repository = game_repository
        self.player_id_created = None

    def enroll_player(self, username, user_id, game_id):
        game = self.game_repository.get(game_id)
        player = Player(name=username, user_id=user_id)
        game.enroll_player(player)
        self.game_repository.update(game)
        return player.user_id
