from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError

from db.session import Session
from core.config import settings

from typing import List

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login/")


def get_db():
    """Provide a database session and ensure it is closed after use."""
    session = Session()
    try:
        yield session
    finally:
        session.close()


def get_auth_user(token: str = Depends(oauth2_scheme)):
    """Decode JWT token and return the authenticated user's ID and role."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("sub")
        user_role = payload.get("role")

        if not user_id or not user_role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        return user_id, user_role

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def role_check(*args: List[str]):
    """
    Dependency generator to enforce role-based access control.

    Usage: Depends(role_check("user", "admin"))
    """

    def role_checker(auth_user: dict = Depends(get_auth_user)):
        if auth_user[1] not in args:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )
        return int(auth_user[0])

    return role_checker
