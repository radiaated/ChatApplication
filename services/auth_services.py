from sqlalchemy.orm import Session

from schemas.user import UserLogin
from core.security import verify_password, create_access_token
from services.user_services import get_user_by_email_or_username


def authenticate_user(db: Session, user: UserLogin):

    db_user = get_user_by_email_or_username(
        db=db, email=user.username, username=user.username
    )

    if not db_user:

        return None

    if not verify_password(password=user.password, hashed_password=db_user.password):

        return None

    claims = {"sub": str(db_user.id), "role": db_user.role.value}

    return create_access_token(claims=claims)
