from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from . import crud, schemas
from .dependencies import get_db

event_router = APIRouter()


@event_router.post(
    "/", response_model=schemas.Event, status_code=status.HTTP_201_CREATED
)
def create_event_view(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event_db(db=db, event_schema=event)


@event_router.get(
    "/", response_model=list[schemas.Event], status_code=status.HTTP_200_OK
)
def events_view(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events_db(db=db, offset=offset, limit=limit)
    return events
