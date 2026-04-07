from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from schemas.chat import (
    ChatMessageRequest,
    ChatRoomCreate,
    ChatRoomUpdate,
    ChatRoomMessageCountResponse,
    UserMessageCount,
    UserRoomCount,
)
from models.chat import Message, Room, room_participants
from models.user import User

from datetime import datetime
from typing import List, Optional


def get_rooms(db: Session) -> List[Room]:
    """Retrieve all chat rooms from the database."""
    try:
        db_room = db.query(Room).all()
        return db_room
    except SQLAlchemyError as ex:
        print(ex)
        return []


def get_room(db: Session, room_id: int) -> Optional[Room]:
    """Retrieve a single chat room by its ID."""
    try:
        db_room = db.get(Room, room_id)
        return db_room
    except SQLAlchemyError as ex:
        print(ex)
        return None


def get_participant_rooms(db: Session, participant_id: int) -> List[Room]:
    """Get all rooms a specific participant belongs to."""
    try:
        # Join Room with participants table to filter rooms by user
        db_rooms = (
            db.query(Room)
            .join(Room.participants)
            .filter(User.id == participant_id)
            .all()
        )
        return db_rooms
    except SQLAlchemyError as ex:
        print(ex)
        return []


def get_participant_room(
    db: Session, room_id: int, participant_id: int
) -> Optional[Room]:
    """Get a specific room where a participant is a member."""
    try:
        # Join Room with participants and filter by room ID and user ID
        db_room = (
            db.query(Room)
            .join(Room.participants)
            .filter(User.id == participant_id, Room.id == room_id)
            .first()
        )
        return db_room
    except SQLAlchemyError as ex:
        print(ex)
        return None


def create_room(
    db: Session, chat_room: ChatRoomCreate, admin_id: int
) -> Optional[Room]:
    """Create a new chat room and add the admin as a participant."""
    try:
        db_room = Room(
            name=chat_room.name, description=chat_room.description, admin_id=admin_id
        )
        # Fetch the admin user to add them as participant
        admin_user = db.get(User, admin_id)
        db_room.participants.append(admin_user)

        db.add(db_room)
        db.commit()
        db.refresh(db_room)
        return db_room
    except SQLAlchemyError as ex:
        db.rollback()
        print(ex)
        return None


def update_room(
    db: Session,
    room_id: int,
    user_id: int,
    chat_room: ChatRoomUpdate,
    admin_check: bool = True,
) -> Optional[Room]:
    """Update room name or description if user is admin or admin check is disabled."""
    try:
        db_room = db.get(Room, room_id)

        if db_room and (not admin_check or db_room.admin_id == user_id):
            if chat_room.name:
                db_room.name = chat_room.name
            if chat_room.description:
                db_room.description = chat_room.description

            db.commit()
            db.refresh(db_room)
            return db_room

        return None
    except SQLAlchemyError as ex:
        db.rollback()
        print(ex)
        return None


def delete_room(
    db: Session, room_id: int, user_id: int, admin_check: bool = True
) -> Optional[Room]:
    """Delete a room if the user is admin or admin check is disabled."""
    try:
        db_room = db.get(Room, room_id)

        if db_room and (not admin_check or db_room.admin_id == user_id):
            db.delete(db_room)
            db.commit()
            return db_room

        return None
    except SQLAlchemyError as ex:
        db.rollback()
        print(ex)
        return None


def get_recent_room_messages(
    db: Session, room_id: int, cursor: Optional[datetime] = None, limit: int = 10
) -> List[Message]:
    """Retrieve recent messages from a room with optional cursor pagination."""
    try:
        query = db.query(Message).filter(Message.room_id == room_id)

        # Filter messages older than cursor for pagination
        if cursor is not None:
            query = query.filter(Message.datetime_delivered < cursor)

        messages = query.order_by(Message.datetime_delivered.desc()).limit(limit).all()
        return messages
    except SQLAlchemyError as ex:
        print(ex)
        return []


def add_room_participant(db: Session, room_id: int, user_id: int) -> bool:
    """Add a user to a room if not already a participant."""
    try:
        db_room = db.get(Room, room_id)
        db_user = db.get(User, user_id)

        if not db_room or not db_user:
            return False

        # Check if user is already a participant
        if any(user.id == user_id for user in db_room.participants):
            return True

        db_room.participants.append(db_user)
        db.commit()
        return True
    except SQLAlchemyError as ex:
        db.rollback()
        print(ex)
        return False


def check_room_participant(db: Session, room_id: int, user_id: int) -> bool:
    """Check if a user is a participant in a room."""
    try:
        db_room = db.get(Room, room_id)
        db_user = db.get(User, user_id)

        if db_user in db_room.participants:
            return True
        return False
    except SQLAlchemyError as ex:
        print(ex)
        return False


def create_message(
    db: Session, room_id: int, message: ChatMessageRequest, sender_id: int
) -> Optional[Message]:
    """Create a new message in a room from a sender."""
    try:
        db_message = Message(
            text=message.text,
            datetime_sent=message.datetime_sent,
            sender_id=sender_id,
            room_id=room_id,
        )

        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    except SQLAlchemyError as ex:
        db.rollback()
        print(ex)
        return None


def get_room_messages_count(
    db: Session,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
) -> List[ChatRoomMessageCountResponse]:
    """Get count of messages per room, optionally filtered by date range."""
    try:
        # Perform outer join to include rooms with zero messages
        db_messages = (
            db.query(Room.id, Room.name, func.count(Message.id))
            .outerjoin(Message, Room.id == Message.room_id)
            .group_by(Room.id)
        )

        # Filter messages by date range if provided
        if start_datetime and end_datetime:
            db_messages = db_messages.filter(
                Message.datetime_delivered.between(start_datetime, end_datetime)
            )

        db_messages = db_messages.all()

        messages = [
            {"id": room_id, "name": name, "message_count": count}
            for room_id, name, count in db_messages
        ]
        return messages
    except SQLAlchemyError as ex:
        print(ex)
        return []


def get_user_messages_count(
    db: Session,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    user_id: int | None = None,
) -> List[UserMessageCount]:
    """Get count of messages sent by users, optionally filtered by date or user."""
    try:
        # Aggregate message counts grouped by user
        db_messages = (
            db.query(User.id, User.username, func.count(Message.id))
            .outerjoin(Message, Message.sender_id == User.id)
            .group_by(User.id)
        )

        if start_datetime and end_datetime:
            db_messages = db_messages.filter(
                Message.datetime_delivered.between(start_datetime, end_datetime)
            )

        # Filter for a specific user if user_id is provided
        if user_id:
            db_message = db_messages.filter(User.id == user_id).first()
            db_messages = [db_message] if db_message else []
        else:
            db_messages = db_messages.all()

        messages = [
            {"user_id": user_id, "username": username, "message_count": count}
            for user_id, username, count in db_messages
        ]
        return messages
    except SQLAlchemyError as ex:
        print(ex)
        return []


def get_user_rooms_count(db: Session, user_id: int) -> List[UserRoomCount]:
    """Get count of rooms a user participates in, optionally filtered by user."""
    try:
        # Aggregate room counts per user
        db_rooms = (
            db.query(
                User.id.label("user_id"),
                User.username,
                func.count(room_participants.c.room_id).label("room_count"),
            )
            .outerjoin(room_participants, room_participants.c.user_id == User.id)
            .group_by(User.id)
        )

        # Filter for specific user if user_id is provided
        if user_id:
            db_room = db_rooms.filter(User.id == user_id).first()
            db_rooms = [db_room] if db_room else []
        else:
            db_rooms = db_rooms.all()

        return db_rooms
    except SQLAlchemyError as ex:
        print(ex)
        return []
