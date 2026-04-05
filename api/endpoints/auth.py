from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from api.deps import get_db
from schemas.user import UserCreate, UserLogin
from services.user_services import create_user

auth_router = APIRouter()


@auth_router.post("/signup/")
def signup(user: UserCreate, db=Depends(get_db)):

    user = create_user(db=db, user=user)

    response = JSONResponse(
        content={"message": "User created."}, status_code=status.HTTP_201_CREATED
    )

    return response
