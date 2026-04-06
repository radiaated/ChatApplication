from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.orm import relationship
from db.base import Base
import enum


class UserRole(enum.Enum):
    """Enum representing user roles."""

    ADMIN = "admin"
    USER = "user"


class User(Base):
    """User model with role, authentication info, and relationships to rooms and messages."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(32), unique=True, nullable=False)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    # One-to-one relationship: latest message sent by user
    messages = relationship("Message", back_populates="user", uselist=False)

    # One-to-one relationship: rooms where user is admin
    admin_rooms = relationship(
        "Room", back_populates="admin", uselist=False, foreign_keys="Room.admin_id"
    )

    # Many-to-many relationship: rooms where user is participant
    participant_rooms = relationship(
        "Room", secondary="room_participants", back_populates="participants"
    )
