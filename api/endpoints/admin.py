from fastapi import APIRouter, Depends

from api.deps import get_db, role_check
from schemas.user import ProfileResponse
from schemas.user import UserCreate
from services.user_services import add_user, get_user_by_id, get_all_users

from typing import List

admin_router = APIRouter()


@admin_router.post("/user/", response_model=ProfileResponse)
async def create_user(
    user: UserCreate, db=Depends(get_db), _=Depends(role_check("admin"))
):

    user = add_user(db=db, user=user)

    return user


@admin_router.get("/user/", response_model=List[ProfileResponse])
async def get_users(db=Depends(get_db), _=Depends(role_check("admin"))):

    users = get_all_users(db=db)

    return users
