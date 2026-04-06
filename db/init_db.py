from db.session import engine

from db.base import Base

from models.user import User
from models.chat import Room, Message, room_participants


Base.metadata.create_all(bind=engine)
