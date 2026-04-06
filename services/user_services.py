from sqlalchemy.orm import Session
from sqlalchemy import or_

from models.user import User, UserRole
from core.security import hash_password
from schemas.user import UserCreate, UserUpdate


def add_user(db: Session, user: UserCreate):

    db_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role=user.role,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def edit_user_by_id(
    db: Session,
    user_id: int,
    user: UserUpdate,
):

    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user:

        if user.username:
            db_user.username = user.username

        if user.email:
            db_user.email = user.email

        if user.role:
            db_user.role = user.role

        db.commit()

        db.refresh(db_user)

        return db_user

    return None


def remove_user_by_id(
    db: Session,
    user_id: int,
):

    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user:

        db.delete(db_user)

        db.commit()

        return db_user

    return None


def get_all_users(db: Session):

    return db.query(User).all()


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
