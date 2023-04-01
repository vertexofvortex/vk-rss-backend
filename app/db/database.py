"""Main init file for database"""

from sqlalchemy import create_engine
from app.settings import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_TABLE}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(engine)

Base = declarative_base()