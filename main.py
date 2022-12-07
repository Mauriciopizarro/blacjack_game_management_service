import time
from fastapi import FastAPI
import infrastructure.injector # no remove this dependecy
from infrastructure.controllers import enroll_player_controller, start_game_controller, create_game_controller
from infrastructure.event_managers.rabbit_publisher import RabbitConnection

time.sleep(10)
RabbitConnection.init_connection()

app = FastAPI()

app.include_router(enroll_player_controller.router)
app.include_router(start_game_controller.router)
app.include_router(create_game_controller.router)
