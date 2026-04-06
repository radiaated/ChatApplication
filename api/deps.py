from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from db.session import Session
from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login/")


def get_db():

    session = Session()

    try:
        yield session
    finally:
        session.close()


def get_auth_user(token: str = Depends(oauth2_scheme)):

    try:

        payload = jwt.decode(token, settings.SECRET_KEY, [settings.JWT_ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:

            raise HTTPException(status_code=402, detail="Invalid token")

        return int(user_id)

    except:

        raise HTTPException(status_code=402, detail="Invalid token")
