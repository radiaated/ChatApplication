from sqladmin import ModelView
from models.user import User
from models.chat import Room, Message


class UserAdmin(ModelView, model=User):
    """Admin view for managing users."""

    column_list = [User.id, User.email, User.username, User.role]


class RoomAdmin(ModelView, model=Room):
    """Admin view for managing chat rooms."""

    column_list = [Room.id, Room.name, Room.description]


class MessageAdmin(ModelView, model=Message):
    """Admin view for managing messages."""

    column_list = [
        Room.id,
        Message.text,
        Message.datetime_sent,
        Message.datetime_delivered,
        Message.sender_id,
    ]
