from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from api.deps import get_db
from schemas.user import UserCreate, UserLogin
from schemas.token import TokenResponse
from services import user_services, auth_services

auth_router = APIRouter()


@auth_router.post("/signup/")
async def signup(user: UserCreate, db=Depends(get_db)):

    user = user_services.create_user(db=db, user=user)

    return JSONResponse(
        content={"detail": "User created."}, status_code=status.HTTP_201_CREATED
    )


@auth_router.post("/signin/", response_model=TokenResponse)
async def signin(user: UserLogin, db=Depends(get_db)):

    access_token = auth_services.authenticate_user(db=db, user=user)

    if not access_token:

        response = JSONResponse(
            content={"detail": "Invalid credentials."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

        return response

    return {"access": access_token}
