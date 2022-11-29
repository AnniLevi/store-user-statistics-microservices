import datetime
from typing import Any

from pydantic import BaseModel


class EventBase(BaseModel):
    type: str
    store_id: int
    user_id: str
    data: dict[str, Any]


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True
