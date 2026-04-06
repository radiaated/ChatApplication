from sqlalchemy.orm import Session
from schemas.chat import ChatMessageResponse, ChatRoomCreate, ChatRoomUpdate
from models.chat import Message, Room
from models.user import User
from datetime import datetime

from services.user_services import get_user_by_id


def get_room_by_id(
    db: Session,
    room_id: int,
):

    db_room = db.query(Room).filter(Room.id == room_id).first()

    return db_room


def get_rooms_by_participant_id(
    db: Session,
    participant_id: int,
):

    db_rooms = (
        db.query(Room).join(Room.participants).filter(User.id == participant_id).all()
    )

    return db_rooms


def add_room(db: Session, chat_room: ChatRoomCreate, admin_id: int):

    db_room = Room(
        name=chat_room.name, description=chat_room.description, admin_id=admin_id
    )

    admin_user = db.get(User, admin_id)
    db_room.participants.append(admin_user)

    db.add(db_room)

    db.commit()

    db.refresh(db_room)

    return db_room


def edit_room(
    db: Session,
    room_id: int,
    user_id: int,
    chat_room: ChatRoomUpdate,
):

    db_room = db.query(Room).filter(Room.id == room_id).first()

    if db_room.admin_id != user_id:

        return None

    if chat_room.name:
        db_room.name = chat_room.name

    if chat_room.description:
        db_room.description = chat_room.description

    db.commit()

    db.refresh(db_room)

    return db_room


def remove_room(
    db: Session,
    room_id: int,
    user_id: int,
):

    db_room = db.query(Room).filter(Room.id == room_id).first()

    if db_room.admin_id != user_id:

        return None

    db.delete(db_room)

    db.commit()

    return db_room


def get_recent_messages_by_room_id(
    db: Session,
    room_id: int,
    cursor: datetime = None,
    limit: int = 10,
):

    if cursor:

        db_messages = (
            db.query(Message)
            .filter(Message.room_id == room_id)
            .filter(Message.datetime_delivered < cursor)
            .order_by(Message.datetime_delivered.desc())
            .limit(limit)
            .all()
        )
    else:
        db_messages = (
            db.query(Message)
            .filter(Message.room_id == room_id)
            .order_by(Message.datetime_delivered.desc())
            .limit(limit)
            .all()
        )

    return db_messages


def add_participant_to_room(db: Session, room_id: int, user_id: int):

    db_room = db.query(Room).filter(Room.id == room_id).first()

    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user not in db_room.participants:

        db_room.participants.append(db_user)

    db.commit()


def add_message(
    db: Session, room_id: int, message: ChatMessageResponse, sender_id: int
):

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
