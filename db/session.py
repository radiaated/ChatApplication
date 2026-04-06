from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

# Create a SQLAlchemy engine using the database URL from settings
engine = create_engine(url=settings.DATABASE_URL)

# Create a session factory bound to the engine
Session = sessionmaker(bind=engine, autoflush=False)
