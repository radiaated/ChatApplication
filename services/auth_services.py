from sqlalchemy import or_
from sqlalchemy.orm import Session
from schemas.user import UserLogin
from models.user import User
from core.security import verify_password, create_access_token


def authenticate_user(db: Session, user: UserLogin):

    db_user = (
        db.query(User)
        .filter(or_(User.username == user.username, User.email == user.username))
        .first()
    )

    if not db_user:

        return None

    if not verify_password(user.password, db_user.password):

        return None

    return create_access_token({"sub": str(db_user.id), "role": db_user.role.value})
