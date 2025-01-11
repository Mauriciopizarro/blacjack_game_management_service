from fastapi import FastAPI
from infrastructure.controllers import enroll_player_controller, start_game_controller, create_game_controller
from infrastructure.event_managers.rabbit_conection import RabbitConnection
from infrastructure.injector import Injector

# We declare queues here
queues = ["game_started"]
channel = RabbitConnection.get_channel()
RabbitConnection.declare_queues(channel, queues)

app = FastAPI()
injector = Injector()
app.container = injector

app.include_router(enroll_player_controller.router)
app.include_router(start_game_controller.router)
app.include_router(create_game_controller.router)
