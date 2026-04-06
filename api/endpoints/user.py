from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from api.deps import get_db, role_check
from schemas.user import UserUpdate, UserResponse
from services import user_services

user_router = APIRouter()


@user_router.get("/profile/", response_model=UserResponse)
async def retrieve_profile(
    db=Depends(get_db), user_id=Depends(role_check("user", "admin"))
):
    """Retrieve the profile of the authenticated user."""
    # Fetch user profile from the database
    user_profile = user_services.get_user(db=db, id=user_id)

    if not user_profile:
        response = JSONResponse(
            content={"detail": "User doesn't exist."},
            status_code=status.HTTP_404_NOT_FOUND,
        )
        return response

    return user_profile


@user_router.put("/profile/", response_model=UserResponse)
async def update_profile(
    user: UserUpdate, db=Depends(get_db), user_id=Depends(role_check("user", "admin"))
):
    """Update the profile of the authenticated user."""
    # Update user profile from the database
    user_profile = user_services.update_user(db=db, user=user, user_id=user_id)

    if not user_profile:
        response = JSONResponse(
            content={"detail": "User doesn't exist."},
            status_code=status.HTTP_404_NOT_FOUND,
        )
        return response

    return user_profile
