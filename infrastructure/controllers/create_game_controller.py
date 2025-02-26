from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from domain.exceptions import GameAlreadyCreated
from dependency_injector.wiring import Provide, inject
from infrastructure.injector import Injector

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


@router.post("/game/create", response_model=CreateGameResponseModel)
@inject
async def create_game(request_data: CreateGameRequestData,
                      create_game_service = Depends(Provide[Injector.create_game_service])):
    try:
        game = create_game_service.create_game(username=request_data.username, user_id=request_data.user_id)
        return CreateGameResponseModel(id=game.id, admin=Admin(name=request_data.username, id=request_data.user_id))
    except GameAlreadyCreated as e:
        raise HTTPException(
            status_code=400, detail=f"Game id {e.game_id_created} is already created, please start them",
        )