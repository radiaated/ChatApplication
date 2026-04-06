from fastapi import APIRouter, Depends

from api.deps import get_db, role_check
from schemas.user import ProfileResponse, UserCreate, UserUpdate
from schemas.chat import ChatRoomCreate, ChatRoomUpdate, ChatRoomResponse
from services.user_services import (
    add_user,
    edit_user_by_id,
    remove_user_by_id,
    get_user_by_id,
    get_all_users,
)
from services.chat_services import (
    add_room,
    edit_room_by_id,
    remove_room_by_id,
    get_room_by_id,
    get_all_rooms,
)

from typing import List

admin_router = APIRouter()


@admin_router.get("/user/", response_model=List[ProfileResponse])
async def get_users(db=Depends(get_db), _=Depends(role_check("admin"))):

    users = get_all_users(db=db)

    return users


@admin_router.get("/user/{id}/", response_model=ProfileResponse)
async def get_user(id: int, db=Depends(get_db), _=Depends(role_check("admin"))):

    user = get_user_by_id(db=db, id=id)

    return user


@admin_router.post("/user/", response_model=ProfileResponse)
async def create_user(
    user: UserCreate, db=Depends(get_db), _=Depends(role_check("admin"))
):

    created_user = add_user(db=db, user=user)

    return created_user


@admin_router.put("/user/{id}/", response_model=ProfileResponse)
async def update_user(
    id: int, user: UserUpdate, db=Depends(get_db), _=Depends(role_check("admin"))
):

    updated_user = edit_user_by_id(db=db, user=user, user_id=id)

    return updated_user


@admin_router.delete("/user/{id}/", response_model=ProfileResponse)
async def delete_user(id: int, db=Depends(get_db), _=Depends(role_check("admin"))):

    user = remove_user_by_id(db=db, user_id=id)

    return user


# Room
@admin_router.get("/room/", response_model=List[ChatRoomResponse])
async def get_rooms(db=Depends(get_db), _=Depends(role_check("admin"))):

    rooms = get_all_rooms(db=db)

    return rooms


@admin_router.get("/room/{id}/", response_model=ChatRoomResponse)
async def get_room(id: int, db=Depends(get_db), _=Depends(role_check("admin"))):

    room = get_room_by_id(db=db, id=id)

    return room


@admin_router.post("/room/", response_model=ChatRoomResponse)
async def create_room(
    room: ChatRoomCreate, db=Depends(get_db), user_id=Depends(role_check("admin"))
):

    created_room = add_room(db=db, chat_room=room, admin_id=user_id, admin_check=False)

    return created_room


@admin_router.put("/room/{id}/", response_model=ChatRoomResponse)
async def update_room(
    id: int,
    room: ChatRoomUpdate,
    db=Depends(get_db),
    user_id=Depends(role_check("admin")),
):

    updated_room = edit_room_by_id(
        db=db, room_id=id, user_id=user_id, chat_room=room, admin_check=False
    )

    return updated_room


@admin_router.delete("/room/{id}/", response_model=ChatRoomResponse)
async def delete_room(
    id: int, db=Depends(get_db), user_id=Depends(role_check("admin"))
):

    room = remove_room_by_id(db=db, room_id=id, user_id=id, admin_check=False)

    return room
