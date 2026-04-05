from passlib.context import CryptContext
from jose import jwt

from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):

    return pwd_context.hash(password)


def verify_password(password: str, hashed_password):

    return pwd_context.verify(password, hashed_password)


def create_access_token(claims: dict):

    return jwt.encode(claims, settings.SECRET_KEY, settings.JWT_ALGORITHM)
