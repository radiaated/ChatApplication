from fastapi import WebSocket, WebSocketException
from jose import jwt

from core.config import settings


def get_auth_user_ws(websocket: WebSocket):

    auth_header = websocket.headers.get("Authorization")

    token = None
    if auth_header:
        parts = auth_header.split()

        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1]

    try:

        payload = jwt.decode(token, settings.SECRET_KEY, [settings.JWT_ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:

            raise WebSocketException(reason="Invalid token.", code=3000)

        return int(user_id)

    except Exception as ex:

        print(ex)

        raise WebSocketException(reason="Invalid token.", code=3000)
