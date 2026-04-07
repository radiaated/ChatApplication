from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from models.user import UserRole
import re
from typing import Optional


class User(BaseModel):
    """Base schema for user data."""

    email: EmailStr
    username: str
    role: Optional[UserRole] = UserRole.USER

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        # Ensure username is 3–32 chars and only contains letters, numbers, underscores
        pattern = re.compile(r"^[a-zA-Z0-9_]{3,32}$")
        if not pattern.match(v):
            raise ValueError(
                "Username must be 3–32 characters and can only contain letters, numbers, and underscores."
            )
        return v


class UserCreate(User):
    """Schema for creating a new user, including password validation."""

    password: str
    password2: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v) -> str:
        # Ensure password has at least 8 chars, 1 uppercase, 1 digit
        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
        if not pattern.match(v):
            raise ValueError(
                "Password must contain at least 8 characters, one uppercase letter, one digit."
            )
        return v

    @field_validator("password2")
    @classmethod
    def passwords_match(cls, v, info) -> str:
        # Ensure password confirmation matches
        password = info.data.get("password")
        if password and v != password:
            raise ValueError("Password and confirm password does not match.")
        return v


class UserUpdate(User):
    """Schema for updating user information (partial update allowed)."""

    email: Optional[EmailStr] = None
    username: Optional[str] = None
    role: Optional[UserRole] = None


class UserNoRoleUpdate(UserUpdate):
    """Schema for partially updating user information without changing the role.

    The 'role' field is not allowed and will always be None.
    Other fields (email, username) can still be updated.
    """

    role: None = None


class UserLogin(BaseModel):
    """Schema for user login."""

    username: str
    password: str


class UserResponse(BaseModel):
    """Schema for returning user details."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    username: str
    role: str
