from sqlalchemy.orm import Session

from ..models import Consumer
from ..schemas import store_schemas


def all_stores_db(db: Session, offset: int, limit: int):
    return (
        db.query(Consumer).filter_by(is_admin=False).offset(offset).limit(limit).all()
    )


def create_store_db(store_schema: store_schemas.StoreCreate, db: Session):
    store_db = Consumer(**store_schema.dict())
    db.add(store_db)
    db.commit()
    db.refresh(store_db)
    return store_db
