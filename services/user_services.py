from typing import Optional, List, Union
from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

from models.user import User
from core.security import hash_password
from schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate) -> Optional[User]:

    try:

        if get_user_by_email_or_username(
            db=db, username=user.username, email=user.email
        ):

            raise HTTPException(
                detail="User with the given username or email already exists",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

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

    except SQLAlchemyError as ex:

        db.rollback()
        print(ex)

        return None


def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:

    try:

        if get_user_by_email_or_username(
            db=db, username=user.username, email=user.email, excluded_user_id=user_id
        ):

            raise HTTPException(
                detail="User with the given username or email already exists",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        db_user = db.get(User, user_id)

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

    except SQLAlchemyError as ex:

        db.rollback()
        print(ex)

        return None


def delete_user(db: Session, user_id: int) -> Optional[User]:

    try:

        db_user = db.get(User, user_id)

        if db_user:
            db.delete(db_user)
            db.commit()
            return db_user

        return None

    except SQLAlchemyError as ex:

        db.rollback()
        print(ex)

        return None


def get_users(db: Session) -> List[User]:

    try:

        return db.query(User).all()

    except SQLAlchemyError as ex:

        print(ex)

        return []


def get_user(db: Session, id: int) -> Optional[dict]:

    try:

        db_user = (
            db.query(User)
            .with_entities(User.email, User.username, User.role)
            .filter(User.id == id)
            .first()
        )

        if db_user:
            return {
                "email": db_user[0],
                "username": db_user[1],
                "role": db_user[2].value,
            }

        return None

    except SQLAlchemyError as ex:

        print(ex)

        return None


def get_user_by_email_or_username(
    db: Session,
    email: str,
    username: str,
    excluded_user_id: Union[int, None] = None,
) -> Optional[User]:

    try:

        query = db.query(User).filter(
            or_(User.username == username, User.email == email)
        )
        if excluded_user_id:
            query = query.filter(User.id != excluded_user_id)
        return query.first()

    except SQLAlchemyError as ex:

        print(ex)
        return None
