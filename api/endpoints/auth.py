from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from api.deps import get_db
from schemas.user import UserCreate, UserLogin
from schemas.token import TokenResponse
from services import user_services, auth_services

auth_router = APIRouter()


@auth_router.post("/signup/")
async def signup(user: UserCreate, db=Depends(get_db)):
    """Register a new user."""
    # Create user in the database
    db_user = user_services.create_user(db=db, user=user)

    # Return 400 if user creation fails
    if not db_user:
        response = JSONResponse(
            content={"detail": "Failed to signup."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        return response

    # Return success message with 201 status code
    return JSONResponse(
        content={"detail": "User created."}, status_code=status.HTTP_201_CREATED
    )


@auth_router.post("/signin/", response_model=TokenResponse)
async def signin(user: UserLogin, db=Depends(get_db)):
    """Authenticate user and return JWT access token."""
    # Authenticate user credentials
    access_token = auth_services.authenticate_user(db=db, user=user)

    # Return 401 if authentication fails
    if not access_token:
        response = JSONResponse(
            content={"detail": "Invalid credentials."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
        return response

    # Return access token on successful authentication
    return {"access": access_token}
