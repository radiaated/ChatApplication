from db.session import engine

from db.base import Base

from models.user import User


Base.metadata.create_all(bind=engine)
