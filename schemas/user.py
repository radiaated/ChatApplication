from pydantic import BaseModel


class User(BaseModel):

    email: str
    username: str


class UserCreate(User):

    password: str
    password2: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str
