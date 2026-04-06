from fastapi import WebSocket

from typing import Dict


class ConnectionManager:
    def __init__(self):
        # Store active connections as {room_id: {user_id: WebSocket}}
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):

        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
        self.active_connections[room_id][user_id] = websocket

    def disconnect(self, room_id: int, user_id: int):

        if (
            room_id in self.active_connections
            and user_id in self.active_connections[room_id]
        ):
            del self.active_connections[room_id][user_id]
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, message: dict, room_id: int):

        if room_id in self.active_connections:
            for connection in self.active_connections[room_id].values():

                await connection.send_json(message)


manager = ConnectionManager()
