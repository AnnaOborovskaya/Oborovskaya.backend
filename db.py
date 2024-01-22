from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_session
from models.model import *
from sqlalchemy import create_engine

ur_a = settings.POSTGRES_DATABASE_URLA

engine_s = create_engine(ur_a, echo=True)

def create_tables():
    Base.metadata.create_all(bind=engine_s)