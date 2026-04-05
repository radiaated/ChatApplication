from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from api.deps import get_db
from schemas.user import UserCreate, UserLogin
from services.user_services import create_user
from services.auth_services import authenticate_user

auth_router = APIRouter()


@auth_router.post("/signup/")
def signup(user: UserCreate, db=Depends(get_db)):

    user = create_user(db=db, user=user)

    response = JSONResponse(
        content={"message": "User created."}, status_code=status.HTTP_201_CREATED
    )

    return response


@auth_router.post("/signin/")
def signin(user: UserLogin, db=Depends(get_db)):

    access_token = authenticate_user(db, user)

    if not access_token:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    response = JSONResponse(content={"message": "Signed in."})

    response.set_cookie("access", access_token, max_age=3600)

    return response
