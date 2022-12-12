from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from . import crud, schemas
from .dependencies import get_db, pagination_query_params

event_router = APIRouter()


@event_router.post(
    "/", response_model=schemas.Event, status_code=status.HTTP_201_CREATED
)
def create_event_view(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event_db(db=db, event_schema=event)


@event_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user_events_view(user_id: str, db: Session = Depends(get_db)):
    events_deleted = crud.delete_user_events_db(db=db, user_id=user_id)
    return {"message": f"{events_deleted} events were deleted"}


@event_router.delete("/by-store/{store_id}", status_code=status.HTTP_200_OK)
def delete_user_events_by_store_view(store_id: int, db: Session = Depends(get_db)):
    events_deleted = crud.delete_user_events_by_store_db(db=db, store_id=store_id)
    return {"message": f"{events_deleted} events were deleted"}


@event_router.get(
    "/amount/{event_type}",
    response_model=list[schemas.EventAmountStatistics],
    status_code=status.HTTP_200_OK,
)
def events_amount_view(
    event_type: str,
    query_params: dict = Depends(pagination_query_params),
    db: Session = Depends(get_db),
):
    """Grouped statistics for a specific type of event - the time sequence of
    occurrence of a given event for all users."""
    return crud.events_amount_db(event_type=event_type, db=db, **query_params)


@event_router.get(
    "/avg-time/{event_type}",
    response_model=list[schemas.EventAvgTimeStatistics],
    status_code=status.HTTP_200_OK,
)
def events_avg_time_view(
    event_type: str,
    query_params: dict = Depends(pagination_query_params),
    db: Session = Depends(get_db),
):
    """Grouped statistics for a specific type of event - the time sequence of
    average occurrence of a given event for one user."""
    return crud.events_avg_time(event_type=event_type, db=db, **query_params)


@event_router.get(
    "/store-events-amount/{store_id}",
    response_model=list[schemas.EventAmountStatistics],
    status_code=status.HTTP_200_OK,
)
def store_events_amount_view(
    store_id: int,
    query_params: dict = Depends(pagination_query_params),
    db: Session = Depends(get_db),
):
    """
    Statistics for the selected store - how many events were sent over time
    """
    return crud.store_events_amount_db(store_id=store_id, db=db, **query_params)
