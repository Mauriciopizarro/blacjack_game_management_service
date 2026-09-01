from application.create_game_service import CreateGameService
from application.enroll_player_service import EnrollPlayerService
from application.start_game_service import StartGameService
from application.lobby_service import LobbyService
from infrastructure.http_clients.game_service_http_client import GameServiceHttpClient
from infrastructure.repositories.game_mongo_repository import GameMongoRepository as GameManagementMongoRepository
from dependency_injector import containers, providers


class Injector(containers.DeclarativeContainer):
    game_management_repo = providers.Singleton(GameManagementMongoRepository)
    game_service_http_client = providers.Singleton(GameServiceHttpClient)
    create_game_service = providers.Factory(CreateGameService,
                                            game_repository=game_management_repo)
    enroll_player_service = providers.Factory(EnrollPlayerService,
                                              game_repository=game_management_repo)
    start_game_service = providers.Factory(StartGameService,
                                           game_repository=game_management_repo,
                                           game_service_http_client=game_service_http_client)
    lobby_service = providers.Factory(LobbyService,
                                      game_repository=game_management_repo)


    wiring_config = containers.WiringConfiguration(modules=[
        "infrastructure.controllers.create_game_controller",
        "infrastructure.controllers.enroll_player_controller",
        "infrastructure.controllers.start_game_controller",
        "infrastructure.controllers.lobby_controller"
    ])
