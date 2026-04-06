from sqlalchemy import Integer, Column, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from db.base import Base
from models.user import User


class Room(Base):

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    description = Column(String(64), nullable=False)

    admin_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    admin = relationship("User", back_populates="rooms")


class Message(Base):

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    date_sent = Column(
        DateTime,
        nullable=False,
    )
    date_delivered = Column(DateTime, nullable=False, default=func.now())

    sender_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    room_id = Column(
        Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", back_populates="user_messages")
    room = relationship("Room", back_populates="room_messages")
