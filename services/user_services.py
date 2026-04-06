from sqlalchemy.orm import Session
from sqlalchemy import or_

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


def get_user_by_email_or_username(db: Session, email: str, username: str):

    return (
        db.query(User)
        .filter(or_(User.username == username, User.email == email))
        .first()
    )


def get_user_by_id(db: Session, id: int):

    db_user = (
        db.query(User)
        .with_entities(User.email, User.username, User.role)
        .filter(User.id == id)
        .first()
    )

    return {
        "email": db_user[0],
        "username": db_user[1],
        "role": db_user[2].value,
    }
