from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketException,
    WebSocketDisconnect,
)

from ws.deps import get_auth_user_ws
from api.deps import get_db
from services import user_services, chat_services
from schemas.chat import ChatMessageRequest, ChatMessageResponse

from core.connection_manager import manager


chat_ws = APIRouter()


@chat_ws.websocket("/{id}")
async def chat_room(
    ws: WebSocket, id: int, user_id=Depends(get_auth_user_ws), db=Depends(get_db)
):

    room = chat_services.get_room(db=db, room_id=id)

    if not room:
        await manager.disconnect(
            room_id=id, user_id=user_id, code=1008, reason="Room doesn't exist."
        )
        return

    user_detail = user_services.get_user(db=db, id=user_id)

    if not user_detail:
        await manager.disconnect(
            room_id=id, user_id=user_id, code=1008, reason="User doesn't exist."
        )
        return

    await manager.connect(websocket=ws, room_id=id, user_id=user_id)

    is_added = chat_services.add_room_participant(db=db, room_id=id, user_id=user_id)

    if not is_added:

        await manager.disconnect(
            room_id=id, user_id=user_id, code=1000, reason="Failed to join the room."
        )
        return

    await manager.broadcast(
        message="%s has joined the room" % user_detail["username"],
        room_id=id,
    )

    db_messages = chat_services.get_recent_room_messages(db=db, room_id=id)

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

            chat_message = ChatMessageRequest(**data)

            db_message = chat_services.create_message(
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

    except WebSocketException as ex:

        print(f"WebSocket error: {ex}")

    except Exception as ex:

        print(f"WebSocket error: {ex}")

    finally:

        manager.disconnect(room_id=id, user_id=id)
