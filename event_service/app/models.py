import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSON

from .config.db_config import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    store_id = Column(Integer)
    user_id = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    data = Column(JSON)
