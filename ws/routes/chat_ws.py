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
from schemas.chat import ChatMessageRequest, ChatMessageResponse, ChatResponse
from core.connection_manager import manager

# WebSocket router for chat functionality
chat_ws = APIRouter()


@chat_ws.websocket("/{id}")
async def chat_room(
    ws: WebSocket, id: int, user_id=Depends(get_auth_user_ws), db=Depends(get_db)
):
    """Handle WebSocket connections for a chat room."""

    # Check if room exists
    room = chat_services.get_room(db=db, room_id=id)
    if not room:
        await manager.disconnect(
            room_id=id, user_id=user_id, code=1008, reason="Room doesn't exist."
        )
        return

    # Check if user exists
    user_detail = user_services.get_user(db=db, id=user_id)
    if not user_detail:
        await manager.disconnect(
            room_id=id, user_id=user_id, code=1008, reason="User doesn't exist."
        )
        return

    # Connect user to the WebSocket manager
    await manager.connect(websocket=ws, room_id=id, user_id=user_id)

    # Add user to room participants in DB
    has_joined = chat_services.add_room_participant(db=db, room_id=id, user_id=user_id)

    if not has_joined:
        await manager.disconnect(
            room_id=id, user_id=user_id, code=1000, reason="Failed to join the room."
        )
        return

    # Notify room that user has joined
    chat_response = ChatResponse(
        type="broadcast_user_join", data="%s has joined the room" % user_detail.username
    )
    await manager.broadcast(
        message=chat_response.model_dump(mode="json"),
        room_id=id,
    )

    # Send recent room messages to the user
    db_messages = chat_services.get_recent_room_messages(db=db, room_id=id)
    if db_messages:
        chat_response = ChatResponse(
            type="fetch_recent_messages",
            data=[ChatMessageResponse.model_validate(msg) for msg in db_messages],
        )

        await manager.send(
            message=chat_response.model_dump(mode="json"), room_id=id, user_id=user_id
        )

    try:
        while True:
            # Receive new message from user
            data = await ws.receive_json()
            chat_message = ChatMessageRequest.model_validate(data)

            # Store message in DB
            db_message = chat_services.create_message(
                db=db,
                room_id=id,
                message=chat_message,
                sender_id=user_id,
            )

            chat_response = ChatResponse(
                type="broadcast_user_message",
                data=ChatMessageResponse.model_validate(db_message),
            )

            await manager.broadcast(
                message=chat_response.model_dump(mode="json"), room_id=id
            )

    except WebSocketDisconnect:
        # Handle client disconnect
        print("Client disconnected")

    except WebSocketException as ex:
        # Handle WebSocket-specific errors
        print(f"WebSocket error: {ex}")

    except Exception as ex:
        # Handle generic errors
        print(f"WebSocket error: {ex}")

    finally:
        # Ensure user is removed from active connections
        manager.disconnect(room_id=id, user_id=id)
