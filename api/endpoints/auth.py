from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from api.deps import get_db
from schemas.user import UserCreate, UserLogin
from schemas.token import TokenResponse
from services.user_services import create_user, get_user_by_email_or_username
from services.auth_services import authenticate_user

auth_router = APIRouter()


@auth_router.post("/signup/")
async def signup(user: UserCreate, db=Depends(get_db)):

    if get_user_by_email_or_username(db=db, username=user.username, email=user.email):
        return JSONResponse(
            content={"detail": "User with the given username or email already exists"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user = create_user(db=db, user=user)

    return JSONResponse(
        content={"detail": "User created."}, status_code=status.HTTP_201_CREATED
    )


@auth_router.post("/signin/", response_model=TokenResponse)
async def signin(user: UserLogin, db=Depends(get_db)):

    access_token = authenticate_user(db=db, user=user)

    if not access_token:

        response = JSONResponse(
            content={"detail": "Invalid user."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

        return response

    return {"access": access_token}
