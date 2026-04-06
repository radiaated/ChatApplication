from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from schemas.chat import ChatMessageRequest, ChatRoomCreate, ChatRoomUpdate
from models.chat import Message, Room
from models.user import User
from datetime import datetime


def get_rooms(db: Session) -> List[Room]:

    try:

        db_room = db.query(Room).all()
        return db_room

    except SQLAlchemyError as ex:

        print(ex)
        return []


def get_room(db: Session, room_id: int) -> Optional[Room]:

    try:

        db_room = db.get(Room, room_id)
        return db_room

    except SQLAlchemyError as ex:
        print(ex)
        return None


def get_participant_rooms(db: Session, participant_id: int) -> List[Room]:

    try:

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

    try:

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

    try:

        db_room = Room(
            name=chat_room.name, description=chat_room.description, admin_id=admin_id
        )
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

    try:

        query = db.query(Message).filter(Message.room_id == room_id)

        if cursor is not None:
            query = query.filter(Message.datetime_delivered < cursor)

        messages = query.order_by(Message.datetime_delivered.desc()).limit(limit).all()

        return messages

    except SQLAlchemyError as ex:

        print(ex)
        return []


def add_room_participant(db: Session, room_id: int, user_id: int) -> bool:

    try:

        db_room = db.get(Room, room_id)
        db_user = db.get(User, user_id)

        if not db_room or not db_user:
            return False

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

    try:

        db_message = Message(
            text=message.message,
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
