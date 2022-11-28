from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from application.enroll_player_service import EnrollPlayerService
from domain.exceptions import IncorrectGameID, CantEnrollPlayersStartedGame, AlreadyEnrolledPlayer

router = APIRouter()


class EnrollPlayerResponse(BaseModel):
    message: str
    name: str
    player_id: str


class EnrollPlayerRequestData(BaseModel):
    username: str
    user_id: str


@router.post("/enroll_player/{game_id}", response_model=EnrollPlayerResponse)
async def enroll_player(game_id: str, request_data: EnrollPlayerRequestData):

    try:
        enroll_player_service = EnrollPlayerService()
        player_id = enroll_player_service.enroll_player(request_data.username, request_data.id, game_id)
        return EnrollPlayerResponse(
            message="Player enrolled successfully",
            name=str(request_data.username),
            player_id=str(player_id)
        )
    except IncorrectGameID:
        raise HTTPException(
            status_code=404, detail='game_id not found',
        )
    except CantEnrollPlayersStartedGame:
        raise HTTPException(
            status_code=400, detail='Can not enroll players in game started'
        )
    except AlreadyEnrolledPlayer:
        raise HTTPException(
            status_code=400, detail='Player already enrolled'
        )
