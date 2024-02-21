from pymongo import MongoClient
from bson.objectid import ObjectId
from domain.exceptions import IncorrectGameID, IncorrectObjectID
from domain.game import Game
from domain.interfaces.game_repository import GameRepository
from domain.player import Player
from config import settings


class GameMongoRepository(GameRepository):

    instance = None

    def __init__(self):
        self.db = self.get_database()

    # Patron singleton
    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = cls()

        return cls.instance

    @staticmethod
    def get_database():
        client = MongoClient(settings.DATABASE_MONGO_URL)
        return client['game_management']["games"]

    def get(self, game_id: str) -> Game:
        if not ObjectId.is_valid(game_id):
            raise IncorrectObjectID()
        game_dict = self.db.find_one({"_id": ObjectId(game_id)})
        if not game_dict:
            raise IncorrectGameID()
        status = game_dict["status"]
        players = []
        for player in game_dict["players"]:
            players.append(self.get_player_object(player))
        admin = self.get_player_object(game_dict["admin"])
        game = Game(status=status, players=players, id=game_id, admin=admin)
        return game

    def get_created_game(self) -> Game:
        game_dict = self.db.find_one({"status": "created"})
        return self.get(str(game_dict["_id"]))

    def has_created_game(self):
        game_dict = self.db.find_one({"status": "created"})
        if game_dict:
            return True
        return False

    def save(self, game: Game) -> Game:
        db_game = self.db.insert_one(game.dict())
        return Game(status=game.status, players=game.players, id=str(db_game.inserted_id), admin=game.admin)

    def update(self, game: Game) -> Game:
        game_dict = game.dict()
        game_dict.pop("id")
        self.db.find_one_and_update({"_id": ObjectId(game.id)}, {"$set": game_dict})
        return Game(status=game.status, players=game.players, id=game.id, admin=game.admin)

    @staticmethod
    def get_player_object(player_dict):
        return Player(name=player_dict["name"], user_id=player_dict["user_id"])

