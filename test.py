# from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError
# import re


# class User(BaseModel):
#     username: str
#     email: str

#     @field_validator("username", mode="before")
#     @classmethod
#     def username_validation(cls, value: str) -> str:
#         pattern = re.compile(r"^[a-zA-Z0-9_]+$")
#         if not pattern.match(value):
#             raise ValueError("Username invalid")
#         return value


# data = {"username": "invalid username!", "email": "test@example.com"}

# try:
#     user = User(**data)
# except ValidationError as e:
#     print(e.errors())  # handle gracefully instead of crashing
