from passlib.context import CryptContext
from jose import jwt

from core.config import settings

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """Hash a plaintext password."""
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password):
    """Verify a plaintext password against a hashed password."""
    return pwd_context.verify(password, hashed_password)


def create_access_token(claims: dict):
    """Create a JWT access token with the given claims."""
    return jwt.encode(
        claims=claims, key=settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
