from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from ws.deps import get_auth_user_ws
from api.deps import get_db
from services.user_services import get_user_by_id
from services.chat_services import (
    add_participant_to_room,
    add_message,
    get_recent_messages_by_room_id,
)
from schemas.chat import ChatMessage, ChatMessageResponse

from core.connection_manager import manager


chat_ws = APIRouter()


@chat_ws.websocket("/{id}")
async def chat_room(
    ws: WebSocket, id: int, user_id=Depends(get_auth_user_ws), db=Depends(get_db)
):

    await manager.connect(websocket=ws, room_id=id, user_id=user_id)

    add_participant_to_room(db=db, room_id=id, user_id=user_id)

    user_detail = get_user_by_id(db=db, id=user_id)

    await manager.broadcast(
        message="%s has joined the room" % user_detail["username"],
        room_id=id,
    )

    db_messages = get_recent_messages_by_room_id(db=db, room_id=id)

    if db_messages:

        messages_repsonse = [
            ChatMessageResponse(
                id=db_msg.id,
                message=db_msg.text,
                datetime_sent=db_msg.datetime_delivered,
                sender_id=db_msg.sender_id,
            ).model_dump(mode="json")
            for db_msg in db_messages
        ]

        await manager.send(message=messages_repsonse, room_id=id, user_id=user_id)

    try:

        while True:
            data = await ws.receive_json()

            chat_message = ChatMessage(**data)

            db_message = add_message(
                db=db,
                room_id=id,
                message=chat_message,
                sender_id=user_id,
            )

            message_response = ChatMessageResponse(
                id=db_message.id,
                message=db_message.text,
                datetime_sent=db_message.datetime_delivered,
                sender_id=db_message.sender_id,
            )

            await manager.broadcast(
                message=message_response.model_dump(mode="json"), room_id=id
            )

    except WebSocketDisconnect:

        print("Client disconnected")

    except Exception as e:

        print(f"WebSocket error: {e}")
