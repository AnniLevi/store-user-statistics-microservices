from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .config.db_config import Base


class Consumer(Base):
    __tablename__ = "consumers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    api_key = relationship("ApiKey", back_populates="owner", uselist=False)


class ApiKey(Base):
    __tablename__ = "api_keys"
    key = Column(String, primary_key=True)
    owner_id = Column(Integer, ForeignKey(Consumer.id))
    owner = relationship("Consumer", back_populates="api_key")
