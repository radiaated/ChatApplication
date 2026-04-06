from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.orm import relationship
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

    messages = relationship("Message", back_populates="user", uselist=False)
    admin_rooms = relationship(
        "Room", back_populates="admin", uselist=False, foreign_keys="Room.admin_id"
    )

    participant_rooms = relationship(
        "Room", secondary="room_participants", back_populates="participants"
    )
