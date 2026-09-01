from fastapi import FastAPI
from infrastructure.controllers import enroll_player_controller, start_game_controller, create_game_controller, lobby_controller
from infrastructure.injector import Injector

app = FastAPI()
injector = Injector()
app.container = injector

app.include_router(enroll_player_controller.router)
app.include_router(start_game_controller.router)
app.include_router(create_game_controller.router)
app.include_router(lobby_controller.router)
