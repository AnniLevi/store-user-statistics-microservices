from sqlalchemy.orm import Session

from . import models, schemas


def create_event_db(db: Session, event_schema: schemas.EventCreate) -> models.Event:
    event_db = models.Event(**event_schema.dict())
    db.add(event_db)
    db.commit()
    db.refresh(event_db)
    return event_db


def get_events_db(db: Session, offset: int, limit: int) -> list[models.Event]:
    return db.query(models.Event).offset(offset).limit(limit).all()
