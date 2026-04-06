from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from ws.deps import get_auth_user_ws

# from core.connection_manager import manager

chat_ws = APIRouter()


@chat_ws.websocket("/{id}")
async def chat_room(ws: WebSocket, id: int, user_id=Depends(get_auth_user_ws)):

    await ws.accept()

    try:

        while True:
            data = await ws.receive_json()

            await ws.send_json({"room_id": id, "user_id": user_id, "data": data})

    except WebSocketDisconnect:

        print("Client disconnected")

    except Exception as e:

        print(f"WebSocket error: {e}")
