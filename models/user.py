from sqlalchemy import Column, String, Integer, Enum
from db.base import Base

import enum


class UserRole(enum.Enum):

    ADMIN = "admin"
    USER = "user"


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(32), unique=True, nullable=False)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
