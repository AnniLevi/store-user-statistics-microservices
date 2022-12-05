from typing import Any

from pydantic import BaseModel


class EventCreate(BaseModel):
    type: str
    user_id: str
    data: dict[str, Any]
