from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from ws.deps import get_auth_user_ws
from api.deps import get_db
from services.user_services import get_user_by_id
from schemas.chat import ChatMessage, ChatMessageResponse

from core.connection_manager import manager

chat_ws = APIRouter()


@chat_ws.websocket("/{id}")
async def chat_room(
    ws: WebSocket, id: int, user_id=Depends(get_auth_user_ws), db=Depends(get_db)
):

    await manager.connect(websocket=ws, room_id=id, user_id=user_id)

    user_detail = get_user_by_id(db=db, id=user_id)

    await manager.broadcast(
        message="%s has joined the room" % user_detail["username"],
        room_id=id,
    )

    try:

        while True:
            data = await ws.receive_json()

            chat_message = ChatMessage(**data)

            message_response = ChatMessageResponse(
                sender_id=user_id,
                sender_username=user_detail["username"],
                message=chat_message.message,
                date_sent=chat_message.date_sent,
            )

            await manager.broadcast(message=message_response.model_dump(), room_id=id)

    except WebSocketDisconnect:

        print("Client disconnected")

    except Exception as e:

        print(f"WebSocket error: {e}")
