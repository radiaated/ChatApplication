from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from api.deps import get_db, get_auth_user

from schemas.chat import ChatRoomCreate, ChatRoomUpdate, ChatRoomResponse
from services.chat_services import (
    get_room_by_id,
    get_rooms_by_participant_id,
    add_room,
    edit_room,
    remove_room,
)

from typing import List


chat_router = APIRouter()


@chat_router.get("/room/{id}/", response_model=ChatRoomResponse)
def get_room(id: int, db=Depends(get_db)):

    db_room = get_room_by_id(db=db, room_id=id)

    if not db_room:
        return JSONResponse(
            content={"detail": "Room doesn't exist."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return db_room


@chat_router.get("/room/", response_model=List[ChatRoomResponse])
def get_rooms(db=Depends(get_db), user_id=Depends(get_auth_user)):

    db_rooms = get_rooms_by_participant_id(db=db, participant_id=user_id)

    return db_rooms


@chat_router.post("/room/", response_model=ChatRoomResponse)
def create_room(
    chat_room: ChatRoomCreate, db=Depends(get_db), user_id=Depends(get_auth_user)
):

    db_room = add_room(db=db, chat_room=chat_room, admin_id=user_id)

    return db_room


@chat_router.put("/room/{id}/", response_model=ChatRoomResponse)
def update_room(
    id: int,
    chat_room: ChatRoomUpdate,
    db=Depends(get_db),
    user_id=Depends(get_auth_user),
):

    db_room = edit_room(db=db, room_id=id, user_id=user_id, chat_room=chat_room)

    if not db_room:
        return JSONResponse(
            content={"detail": "Unauthorized access."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return db_room


@chat_router.delete("/room/{id}/", response_model=ChatRoomResponse)
def delete_room(
    id: int,
    chat_room: ChatRoomUpdate,
    db=Depends(get_db),
    user_id=Depends(get_auth_user),
):

    db_room = remove_room(db=db, room_id=id, user_id=user_id, chat_room=chat_room)

    if not db_room:
        return JSONResponse(
            content={"detail": "Unauthorized access."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return db_room
