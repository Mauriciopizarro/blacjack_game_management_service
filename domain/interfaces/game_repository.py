from abc import ABC, abstractmethod
from domain.game import Game


class GameRepository(ABC):

    @abstractmethod
    def save(self, game: Game) -> Game:
        pass

    @abstractmethod
    def get(self, game_id: int) -> Game:
        pass
    @abstractmethod
    def has_created_game(self):
        pass
    @abstractmethod
    def get_created_game(self) -> Game:
        pass
    @abstractmethod
    def update(self, game: Game) -> Game:
        pass
