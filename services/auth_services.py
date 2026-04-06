from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from schemas.user import UserLogin
from core.security import verify_password, create_access_token
from services.user_services import get_user_by_email_or_username

from typing import Optional


def authenticate_user(db: Session, user: UserLogin) -> Optional[str]:
    """
    Authenticate a user and return an access token if credentials are valid.
    """
    try:
        # Retrieve the user from the database by email or username
        db_user = get_user_by_email_or_username(
            db=db, email=user.username, username=user.username
        )

        # Return None if user does not exist
        if not db_user:
            return None

        # Verify the provided password against the stored hashed password
        if not verify_password(
            password=user.password, hashed_password=db_user.password
        ):
            return None

        # Prepare JWT claims with user ID and role
        claims = {"sub": str(db_user.id), "role": db_user.role.value}

        # Generate and return access token
        return create_access_token(claims=claims)

    except SQLAlchemyError as ex:
        # Print exception if a database error occurs
        print(ex)
        return None
