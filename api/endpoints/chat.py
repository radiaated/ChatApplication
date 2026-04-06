from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from api.deps import get_db, role_check

from schemas.chat import (
    ChatRoomCreate,
    ChatRoomUpdate,
    ChatRoomResponse,
    ChatMessageResponse,
)
from services import chat_services

from typing import List
from datetime import datetime

chat_router = APIRouter()


@chat_router.get("/room/", response_model=List[ChatRoomResponse])
def list_participant_rooms(
    db=Depends(get_db), user_id=Depends(role_check("user", "admin"))
):
    """List all chat rooms the current participant is part of."""
    db_rooms = chat_services.get_participant_rooms(db=db, participant_id=user_id)
    return db_rooms


@chat_router.get("/room/{id}/", response_model=ChatRoomResponse)
def retrieve_participant_room(
    id: int, db=Depends(get_db), user_id=Depends(role_check("user", "admin"))
):
    """Retrieve a specific chat room for the authenticated participant."""
    db_room = chat_services.get_participant_room(
        db=db, room_id=id, participant_id=user_id
    )

    if not db_room:
        response = JSONResponse(
            content={"detail": "Room doesn't exist."},
            status_code=status.HTTP_404_NOT_FOUND,
        )
        return response

    return db_room


@chat_router.post("/room/", response_model=ChatRoomResponse)
def create_room(
    chat_room: ChatRoomCreate,
    db=Depends(get_db),
    user_id=Depends(role_check("user", "admin")),
):
    """Create a new chat room with the authenticated user as admin."""
    db_room = chat_services.create_room(db=db, chat_room=chat_room, admin_id=user_id)

    if not db_room:
        response = JSONResponse(
            content={"detail": "Failed to create a room."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        return response

    return db_room


@chat_router.put("/room/{id}/", response_model=ChatRoomResponse)
def update_room(
    id: int,
    chat_room: ChatRoomUpdate,
    db=Depends(get_db),
    user_id=Depends(role_check("user", "admin")),
):
    """Update an existing chat room if the user has proper access."""
    db_room = chat_services.update_room(
        db=db, room_id=id, user_id=user_id, chat_room=chat_room
    )

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
    user_id=Depends(role_check("user", "admin")),
):
    """Delete a chat room if the user has proper access."""
    db_room = chat_services.delete_room(
        db=db, room_id=id, user_id=user_id, chat_room=chat_room
    )

    if not db_room:
        return JSONResponse(
            content={"detail": "Unauthorized access."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return db_room


@chat_router.get("/room/{id}/messages/", response_model=List[ChatMessageResponse])
def retrieve_recent_room_messages(
    id: int,
    limit: int | None,
    cursor: str | None = None,
    db=Depends(get_db),
    user_id=Depends(role_check("user", "admin")),
):
    """Retrieve recent messages from a specific chat room for an authorized participant."""
    # Check if participant is part of the room
    if not chat_services.check_room_participant(db=db, room_id=id, user_id=user_id):
        return JSONResponse(
            content={"detail": "Unauthorized access."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    db_messages = chat_services.get_recent_room_messages(
        db=db,
        room_id=id,
        cursor=datetime.fromisoformat(cursor) if cursor else None,
        limit=limit,
    )

    # Format messages for response
    messages = [
        {
            "id": db_msg.id,
            "message": db_msg.text,
            "datetime_sent": db_msg.datetime_delivered,
            "sender_id": db_msg.sender_id,
        }
        for db_msg in db_messages
    ]

    return messages
