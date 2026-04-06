from fastapi import WebSocket, WebSocketException
from jose import jwt, JWTError, ExpiredSignatureError

from core.config import settings


def get_auth_user_ws(websocket: WebSocket):
    """Extract and verify JWT token from WebSocket 'Authorization' header."""

    # Get Authorization header
    auth_header = websocket.headers.get("Authorization")

    token = None
    if auth_header:
        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1]

    if not token:
        raise WebSocketException(reason="Missing token.", code=3000)

    try:
        # Decode JWT token and verify expiration
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise WebSocketException(reason="Invalid token.", code=3000)

        return int(user_id)

    except ExpiredSignatureError:
        raise WebSocketException(reason="Token has expired.", code=3001)

    except JWTError:
        raise WebSocketException(reason="Invalid token.", code=3000)

    except Exception as ex:
        print(ex)
        raise WebSocketException(reason="Invalid token.", code=3000)
