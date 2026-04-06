from fastapi import APIRouter, Depends

from api.deps import get_db, role_check
from schemas.user import ProfileResponse
from services.user_services import get_user_by_id

user_router = APIRouter()


@user_router.get("/profile/", response_model=ProfileResponse)
async def signup(db=Depends(get_db), user_id=Depends(role_check("user", "admin"))):

    user_profile = get_user_by_id(db=db, id=user_id)

    return user_profile
