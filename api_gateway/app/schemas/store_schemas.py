from pydantic import BaseModel


class Store(BaseModel):
    id: int
    name: str
    is_active: bool

    class Config:
        orm_mode = True
