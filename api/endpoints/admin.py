from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from api.deps import get_db, role_check
from schemas.user import UserResponse, UserCreate, UserUpdate
from schemas.chat import (
    ChatRoomCreate,
    ChatRoomUpdate,
    ChatRoomResponse,
    ChatRoomMessageCountResponse,
    UserActivityResponse,
)
from services import user_services, chat_services

from typing import List
from datetime import datetime

admin_router = APIRouter()


@admin_router.get("/user/", response_model=List[UserResponse])
async def list_users(db=Depends(get_db), _=Depends(role_check("admin"))):

    users = user_services.get_users(db=db)

    return users


@admin_router.get("/user/{id}/", response_model=UserResponse)
async def retrieve_user(id: int, db=Depends(get_db), _=Depends(role_check("admin"))):

    user = user_services.get_user(db=db, id=id)

    if not user:

        response = JSONResponse(
            content={"detail": "User doesn't exist."},
            status_code=status.HTTP_404_NOT_FOUND,
        )
        return response

    return user


@admin_router.post("/user/", response_model=UserResponse)
async def create_user(
    user: UserCreate, db=Depends(get_db), _=Depends(role_check("admin"))
):

    db_user = user_services.create_user(db=db, user=user)

    if not db_user:

        response = JSONResponse(
            content={"detail": "Failed to create a user."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        return response

    return db_user


@admin_router.put("/user/{id}/", response_model=UserResponse)
async def update_user(
    id: int, user: UserUpdate, db=Depends(get_db), _=Depends(role_check("admin"))
):

    db_user = user_services.update_user(db=db, user=user, user_id=id)

    if not db_user:

        response = JSONResponse(
            content={"detail": "User doesn't exist."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

        return response

    return db_user


@admin_router.delete("/user/{id}/", response_model=UserResponse)
async def delete_user(id: int, db=Depends(get_db), _=Depends(role_check("admin"))):

    db_user = user_services.delete_user(db=db, user_id=id)

    if not db_user:

        response = JSONResponse(
            content={"detail": "User doesn't exist."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

        return response

    return db_user


# Room
@admin_router.get("/room/", response_model=List[ChatRoomResponse])
async def list_rooms(db=Depends(get_db), _=Depends(role_check("admin"))):

    rooms = chat_services.get_rooms(db=db)

    return rooms


@admin_router.get("/room/{id}/", response_model=ChatRoomResponse)
async def retrieve_room(id: int, db=Depends(get_db), _=Depends(role_check("admin"))):

    room = chat_services.get_room(db=db, id=id)

    if not room:

        response = JSONResponse(
            content={"detail": "Room doesn't exist."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

        return response

    return room


@admin_router.post("/room/", response_model=ChatRoomResponse)
async def create_room(
    room: ChatRoomCreate, db=Depends(get_db), user_id=Depends(role_check("admin"))
):

    db_room = chat_services.create_room(
        db=db, chat_room=room, admin_id=user_id, admin_check=False
    )

    if not db_room:

        response = JSONResponse(
            content={"detail": "Failed to create a room."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        return response

    return db_room


@admin_router.put("/room/{id}/", response_model=ChatRoomResponse)
async def update_room(
    id: int,
    room: ChatRoomUpdate,
    db=Depends(get_db),
    user_id=Depends(role_check("admin")),
):

    db_room = chat_services.update_room(
        db=db, room_id=id, user_id=user_id, chat_room=room, admin_check=False
    )

    if not db_room:

        response = JSONResponse(
            content={"detail": "Room doesn't exist."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

        return response

    return db_room


@admin_router.delete("/room/{id}/", response_model=ChatRoomResponse)
async def delete_room(
    id: int, db=Depends(get_db), user_id=Depends(role_check("admin"))
):

    room = chat_services.delete_room(
        db=db, room_id=id, user_id=user_id, admin_check=False
    )

    if not room:

        response = JSONResponse(
            content={"detail": "Room doesn't exist."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

        return response

    return room


# Dashboard


@admin_router.get(
    "/dashboard/room-message/", response_model=List[ChatRoomMessageCountResponse]
)
async def retrieve_dashboard_room_message(
    start: str | None = None,
    end: str | None = None,
    db=Depends(get_db),
    _=Depends(role_check("admin")),
):

    start_datetime = datetime.fromisoformat(start) if start else None
    end_datetime = datetime.fromisoformat(end) if end else None

    room_messages_count = chat_services.get_room_messages_count(
        db=db, start_datetime=start_datetime, end_datetime=end_datetime
    )

    return room_messages_count


@admin_router.get("/dashboard/user-participation/", response_model=UserActivityResponse)
async def retrieve_dashboard_user_participation(
    user_id: int | None = None,
    start: str | None = None,
    end: str | None = None,
    db=Depends(get_db),
    _=Depends(role_check("admin")),
):

    start_datetime = datetime.fromisoformat(start) if start else None
    end_datetime = datetime.fromisoformat(end) if end else None

    messages_count = chat_services.get_user_messages_count(
        db=db, user_id=user_id, start_datetime=start_datetime, end_datetime=end_datetime
    )

    rooms_count = chat_services.get_user_rooms_count(db=db, user_id=user_id)

    return {
        "messages_count": messages_count,
        "rooms_count": rooms_count,
    }
