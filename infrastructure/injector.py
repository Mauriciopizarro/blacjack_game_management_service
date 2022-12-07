from infrastructure.event_managers.rabbit_publisher import RabbitPublisher
from infrastructure.repositories.game_mongo_repository import GameMongoRepository as GameManagementMongoRepository
from dependency_injector import containers, providers


class Injector(containers.DeclarativeContainer):
    game_management_repo = providers.Singleton(GameManagementMongoRepository)
    publisher = providers.Singleton(RabbitPublisher)


injector = Injector()
injector.wire(modules=["application.create_game_service",
                       "application.start_game_service",
                       "application.enroll_player_service",
                       ])
