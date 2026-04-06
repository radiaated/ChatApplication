from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from models.user import UserRole
import re

from typing import Optional


class User(BaseModel):

    email: EmailStr
    username: str
    role: Optional[UserRole] = UserRole.USER

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        pattern = re.compile(r"^[a-zA-Z0-9_]{3,32}$")
        if not pattern.match(v):
            raise ValueError(
                "Username must be 3–32 characters and can only contain letters, numbers, and underscores."
            )
        return v


class UserCreate(User):

    password: str
    password2: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v) -> str:

        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")

        if not pattern.match(v):
            raise ValueError(
                "Password must contain at least 8 characters, one uppercase letter, one digit."
            )

        return v

    @field_validator("password2")
    @classmethod
    def passwords_match(cls, v, info) -> str:

        password = info.data.get("password")

        if password and v != password:
            raise ValueError("Password and confirm password does not match.")

        return v


class UserUpdate(User):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    role: Optional[UserRole] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    email: str
    username: str
    role: str
