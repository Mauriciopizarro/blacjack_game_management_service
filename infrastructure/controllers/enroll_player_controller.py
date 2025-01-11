from pydantic import BaseModel
from dependency_injector.wiring import Provide, inject
from infrastructure.injector import Injector
from fastapi import APIRouter, HTTPException, Depends
from domain.exceptions import IncorrectGameID, CantEnrollPlayersStartedGame, AlreadyEnrolledPlayer, IncorrectObjectID

router = APIRouter()


class EnrollPlayerResponse(BaseModel):
    message: str
    name: str
    player_id: str


class EnrollPlayerRequestData(BaseModel):
    username: str
    user_id: str


@router.post("/game/enroll_player/{game_id}", response_model=EnrollPlayerResponse)
@inject
async def enroll_player(game_id: str,
                        request_data: EnrollPlayerRequestData,
                        enroll_player_service = Depends(Provide[Injector.enroll_player_service])):
    try:
        player_id = enroll_player_service.enroll_player(request_data.username, request_data.user_id, game_id)
        return EnrollPlayerResponse(
            message="Player enrolled successfully",
            name=str(request_data.username),
            player_id=str(player_id)
        )
    except IncorrectGameID:
        raise HTTPException(
            status_code=404, detail='game_id not found',
        )
    except IncorrectObjectID:
        raise HTTPException(
            status_code=400, detail='incorrect game_id',
        )
    except CantEnrollPlayersStartedGame:
        raise HTTPException(
            status_code=400, detail='Can not enroll players in game started'
        )
    except AlreadyEnrolledPlayer:
        raise HTTPException(
            status_code=400, detail='Player already enrolled'
        )
