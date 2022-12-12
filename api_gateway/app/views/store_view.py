import requests
from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from ..config import base_config
from ..db_crud import store_db
from ..dependencies import (
    active_required,
    admin_required,
    get_db,
    pagination_query_params,
)
from ..schemas import store_schemas
from ..utils.exc import exceptions

store_router = APIRouter()


@store_router.get(
    "/",
    response_model=list[store_schemas.Store],
    dependencies=[Depends(active_required), Depends(admin_required)],
    status_code=status.HTTP_200_OK,
)
def all_stores_view(
    query_params: dict = Depends(pagination_query_params),
    db: Session = Depends(get_db),
):
    return store_db.all_stores_db(db=db, **query_params)


@store_router.post(
    "/",
    response_model=store_schemas.Store,
    dependencies=[Depends(active_required), Depends(admin_required)],
    status_code=status.HTTP_201_CREATED,
)
def create_store_view(store: store_schemas.StoreCreate, db: Session = Depends(get_db)):
    return store_db.create_store_db(db=db, store_schema=store)


@store_router.post(
    "/block",
    dependencies=[Depends(active_required), Depends(admin_required)],
    status_code=status.HTTP_201_CREATED,
)
def create_store_view(store_id: int = Body(embed=True), db: Session = Depends(get_db)):
    result = store_db.block_store_db(store_id=store_id, db=db)
    if not result:
        raise exceptions["not_found_exc"]
    return {"message": "Store successfully blocked"}


@store_router.delete(
    "/{store_id}",
    dependencies=[Depends(active_required), Depends(admin_required)],
    status_code=status.HTTP_200_OK,
)
def delete_user_events_by_store(store_id: int):
    user_url = f"{base_config.USER_SERVICE_URL}/api/user/by-store/{store_id}"
    event_url = f"{base_config.EVENT_SERVICE_URL}/api/event/by-store/{store_id}"
    user_response = requests.delete(url=user_url).json()
    event_response = requests.delete(url=event_url).json()
    return {"users": user_response["message"], "events": event_response["message"]}
