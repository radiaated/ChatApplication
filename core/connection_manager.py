from fastapi import WebSocket

from typing import Dict, List


class ConnectionManager:
    """Manage active WebSocket connections per chat room and participant."""

    def __init__(self):
        # Active connections stored as {room_id: {user_id: WebSocket}}
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        # Accept WebSocket and add to active connections
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
        self.active_connections[room_id][user_id] = websocket

    def disconnect(self, room_id: int, user_id: int, *args):
        # Remove WebSocket from active connections
        if (
            room_id in self.active_connections
            and user_id in self.active_connections[room_id]
        ):
            self.active_connections[room_id][user_id].close(*args)
            del self.active_connections[room_id][user_id]
            # Delete room if empty
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, message: dict, room_id: int):
        # Send message to all users in a room
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id].values():
                await connection.send_json(message)

    async def send(self, message: List[dict], room_id: int, user_id: int):
        # Send message to a specific user
        acitve_connection = self.active_connections[room_id][user_id]
        await acitve_connection.send_json(message)


# Singleton manager instance for WebSocket connections
manager = ConnectionManager()
