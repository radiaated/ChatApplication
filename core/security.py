from passlib.context import CryptContext
from jose import jwt

from core.config import settings

from datetime import datetime, timedelta, timezone

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """Hash a plaintext password."""
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password):
    """Verify a plaintext password against a hashed password."""
    return pwd_context.verify(password, hashed_password)


def create_access_token(claims: dict, expires_delta: timedelta = None):
    """Create a JWT access token with expiration."""
    calims_new = claims.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(seconds=settings.JWT_EXPIRES_IN)

    calims_new.update({"exp": expire})

    return jwt.encode(
        claims=calims_new, key=settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
