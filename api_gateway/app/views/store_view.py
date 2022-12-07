from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..db_crud import store_db
from ..dependencies import (
    active_required,
    admin_required,
    get_db,
    pagination_query_params,
)
from ..schemas import store_schemas

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
