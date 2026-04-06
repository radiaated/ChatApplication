from db.session import engine

from db.base import Base

from models.user import User
from models.chat import Room, Message, room_participants

# Create all tables in the database based on SQLAlchemy models
Base.metadata.create_all(bind=engine)
