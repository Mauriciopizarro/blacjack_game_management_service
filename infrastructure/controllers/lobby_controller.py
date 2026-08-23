from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from dependency_injector.wiring import Provide, inject
from infrastructure.injector import Injector
from domain.exceptions import IncorrectGameID, IncorrectObjectID

router = APIRouter()


class LobbyPlayer(BaseModel):
    name: str
    user_id: str


class LobbyAdmin(BaseModel):
    name: str
    user_id: str


class LobbyResponse(BaseModel):
    game_id: str
    status: str
    admin: LobbyAdmin
    players: List[LobbyPlayer]


class LobbyListItem(BaseModel):
    game_id: str
    status: str
    admin: LobbyAdmin


class LobbyListResponse(BaseModel):
    user_id: str
    games: List[LobbyListItem]


@router.get("/game/lobby/list/{user_id}", response_model=LobbyListResponse)
@inject
async def get_lobby_list(user_id: str,
                         lobby_service=Depends(Provide[Injector.lobby_service])):
    return lobby_service.get_lobby_list(user_id)


@router.get("/game/lobby/{game_id}", response_model=LobbyResponse)
@inject
async def get_lobby(game_id: str,
                    lobby_service=Depends(Provide[Injector.lobby_service])):
    try:
        return lobby_service.get_lobby(game_id)
    except IncorrectGameID:
        raise HTTPException(
            status_code=404, detail='game_id not found',
        )
    except IncorrectObjectID:
        raise HTTPException(
            status_code=400, detail='incorrect game_id',
        )