from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from db.session import Session
from core.config import settings

from typing import List

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
        user_role = payload.get("role")

        if not user_id or not user_role:

            raise HTTPException(status_code=401, detail="Invalid token")

        return user_id, user_role

    except Exception as ex:

        print(ex)

        raise HTTPException(status_code=401, detail="Invalid token")


def role_check(*args: List[str]):
    def role_checker(auth_user: dict = Depends(get_auth_user)):
        if auth_user[1] not in args:
            raise HTTPException(status_code=403, detail="Forbidden")
        return int(auth_user[0])

    return role_checker
