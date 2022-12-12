from sqlalchemy import Float, cast, desc, distinct, func
from sqlalchemy.orm import Session
from sqlalchemy.sql import label

from . import schemas
from .models import Event


def create_event_db(db: Session, event_schema: schemas.EventCreate) -> Event:
    event_db = Event(**event_schema.dict())
    db.add(event_db)
    db.commit()
    db.refresh(event_db)
    return event_db


def delete_user_events_db(user_id: str, db: Session):
    user_events = db.query(Event).filter_by(user_id=user_id).delete()
    db.commit()
    return user_events


def delete_user_events_by_store_db(store_id: int, db: Session):
    user_events = db.query(Event).filter_by(store_id=store_id).delete()
    db.commit()
    return user_events


def events_amount_db(event_type: str, db: Session, offset: int, limit: int):
    """The number of times this event occurred each day for all users."""
    return (
        db.query(
            func.date(Event.created_at).label("date"),
            func.count(Event.id).label("event_amount"),
        )
        .filter_by(type=event_type)
        .group_by("date")
        .order_by(desc("date"))
        .offset(offset)
        .limit(limit)
        .all()
    )


def events_avg_time(event_type: str, db: Session, offset: int, limit: int):
    """The number of times this event occurred divided by the number of users
    who had this event for each day."""
    return (
        db.query(
            func.date(Event.created_at).label("date"),
            label(
                "event_avg_time",
                cast(func.count(Event.id), Float)
                / cast(func.count(distinct(Event.user_id)), Float),
            ),
        )
        .filter_by(type=event_type)
        .group_by("date")
        .order_by(desc("date"))
        .offset(offset)
        .limit(limit)
        .all()
    )


def store_events_amount_db(store_id: int, db: Session, offset: int, limit: int):
    """Total amount of events for given store for each date."""
    return (
        db.query(
            func.date(Event.created_at).label("date"),
            func.count(Event.id).label("event_amount"),
        )
        .filter_by(store_id=store_id)
        .group_by("date")
        .order_by(desc("date"))
        .offset(offset)
        .limit(limit)
        .all()
    )
