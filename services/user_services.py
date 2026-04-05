from sqlalchemy.orm import Session
from models.user import User, UserRole

from core.security import hash_password

from schemas.user import UserCreate


def create_user(db: Session, user: UserCreate):

    db_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role=UserRole.USER,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
