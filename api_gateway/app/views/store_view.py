from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..db_crud import store_db
from ..dependencies import get_db, pagination_query_params
from ..schemas import store_schemas
from ..utils.jwt import active_required, admin_required

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
