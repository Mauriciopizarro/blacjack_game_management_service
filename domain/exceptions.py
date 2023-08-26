class CantEnrollPlayersStartedGame(Exception):
    pass


class AlreadyEnrolledPlayer(Exception):
    pass


class IncorrectAdminId(Exception):
    pass


class GameAlreadyStarted(Exception):
    pass


class IncorrectGameID(Exception):
    pass


class IncorrectObjectID(Exception):
    pass

class GameAlreadyCreated(Exception):
    def __init__(self, game_id_created):
        self.game_id_created = game_id_created
