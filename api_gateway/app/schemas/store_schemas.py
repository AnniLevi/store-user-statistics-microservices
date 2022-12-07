from pydantic import BaseModel


class StoreBase(BaseModel):
    name: str
    is_active: bool = True


class StoreCreate(StoreBase):
    is_admin: bool = False


class Store(StoreBase):
    id: int

    class Config:
        orm_mode = True
