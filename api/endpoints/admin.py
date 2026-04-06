from fastapi import APIRouter, Depends

from api.deps import get_db, role_check
from schemas.user import ProfileResponse, UserCreate, UserUpdate
from services.user_services import (
    add_user,
    edit_user_by_id,
    remove_user_by_id,
    get_user_by_id,
    get_all_users,
)

from typing import List

admin_router = APIRouter()


@admin_router.get("/user/", response_model=List[ProfileResponse])
async def get_users(db=Depends(get_db), _=Depends(role_check("admin"))):

    users = get_all_users(db=db)

    return users


@admin_router.get("/user/{id}/", response_model=ProfileResponse)
async def get_user(id: int, db=Depends(get_db), _=Depends(role_check("admin"))):

    user = get_user_by_id(db=db, id=id)

    return user


@admin_router.post("/user/", response_model=ProfileResponse)
async def create_user(
    user: UserCreate, db=Depends(get_db), _=Depends(role_check("admin"))
):

    user = add_user(db=db, user=user)

    return user


@admin_router.put("/user/{id}/", response_model=ProfileResponse)
async def update_user(
    id: int, user: UserUpdate, db=Depends(get_db), _=Depends(role_check("admin"))
):

    user = edit_user_by_id(db=db, user=user, user_id=id)

    return user


@admin_router.delete("/user/{id}/", response_model=ProfileResponse)
async def delete_user(
    id: int, user: UserUpdate, db=Depends(get_db), _=Depends(role_check("admin"))
):

    user = remove_user_by_id(db=db, user=user, user_id=id)

    return user
