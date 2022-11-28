from fastapi import APIRouter, Depends
from pydantic import BaseModel
from application.create_game_service import CreateGameService

router = APIRouter()


class Admin(BaseModel):
    name: str
    id: str


class CreateGameResponseModel(BaseModel):
    message: str = "Game created"
    id: str
    admin: Admin


class CreateGameRequestData(BaseModel):
    username: str
    user_id: str


@router.post("/create_game", response_model=CreateGameResponseModel)
async def create_game(request_data: CreateGameRequestData):
    create_game_service = CreateGameService()
    game = create_game_service.create_game(username=request_data.username, user_id=request_data.user_id)
    return CreateGameResponseModel(id=game.id, admin=Admin(name=request_data.username, id=request_data.user_id))
