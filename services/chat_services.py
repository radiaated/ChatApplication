from sqlalchemy.orm import Session
from schemas.chat import ChatMessageResponse, ChatRoomCreate, ChatRoomUpdate
from models.chat import Message, Room
from models.user import User


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


def add_message(db: Session, room_id: int, message: ChatMessageResponse):

    db_message = Message(
        text=message,
        date_sent=message.date_sent,
        sender_id=message.sender_id,
        room_id=room_id,
    )

    db.add(db_message)

    db.commit()

    db.refresh(db_message)

    return db_message
