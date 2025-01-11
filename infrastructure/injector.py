from application.create_game_service import CreateGameService
from application.enroll_player_service import EnrollPlayerService
from application.start_game_service import StartGameService
from infrastructure.event_managers.rabbit_publisher import RabbitPublisher
from infrastructure.repositories.game_mongo_repository import GameMongoRepository as GameManagementMongoRepository
from dependency_injector import containers, providers


class Injector(containers.DeclarativeContainer):
    game_management_repo = providers.Singleton(GameManagementMongoRepository)
    publisher = providers.Singleton(RabbitPublisher)
    create_game_service = providers.Factory(CreateGameService,
                                            game_repository=game_management_repo)
    enroll_player_service = providers.Factory(EnrollPlayerService,
                                              game_repository=game_management_repo)
    start_game_service = providers.Factory(StartGameService,
                                           game_repository=game_management_repo,
                                           publisher=publisher)


    wiring_config = containers.WiringConfiguration(modules=[
        "infrastructure.controllers.create_game_controller",
        "infrastructure.controllers.enroll_player_controller",
        "infrastructure.controllers.start_game_controller"
    ])
