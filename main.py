from fastapi import FastAPI
import infrastructure.injector # no remove this dependecy
from infrastructure.controllers import enroll_player_controller, start_game_controller, create_game_controller
from infrastructure.event_managers.rabbit_conection import RabbitConnection

# We declare queues here
queues = ["game_started"]
channel = RabbitConnection.get_channel()
RabbitConnection.declare_queues(channel, queues)

app = FastAPI()

app.include_router(enroll_player_controller.router)
app.include_router(start_game_controller.router)
app.include_router(create_game_controller.router)
