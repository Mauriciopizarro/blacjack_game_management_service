from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from application.start_game_service import StartGameService
from domain.exceptions import IncorrectGameID, GameAlreadyStarted, IncorrectAdminId, IncorrectObjectID

router = APIRouter()


class StartGameRequestData(BaseModel):
    user_id: str


@router.post("/game/start/{game_id}")
def start_game(game_id: str, request_data: StartGameRequestData):

    try:
        star_game_service = StartGameService()
        star_game_service.start_game(game_id, request_data.user_id)
    except IncorrectGameID:
        raise HTTPException(
            status_code=404, detail='game_id not found',
        )
    except IncorrectObjectID:
        raise HTTPException(
            status_code=400, detail='incorrect game_id',
        )
    except GameAlreadyStarted:
        raise HTTPException(
            status_code=400, detail='Game already started'
        )
    except IncorrectAdminId:
        raise HTTPException(
            status_code=400, detail='User not enabled for this action'
        )
    return {'message': "Game started"}
