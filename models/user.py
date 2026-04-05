from sqlalchemy import Column, VARCHAR, Integer, Enum
from db.base import Base

import enum


class UserRole(enum.Enum):

    ADMIN = "admin"
    USER = "user"


class User(Base):

    __tablename__ = "tbl_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(32), unique=True, nullable=False)
    username = Column(VARCHAR(32), unique=True, nullable=False)
    password = Column(VARCHAR(60), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
