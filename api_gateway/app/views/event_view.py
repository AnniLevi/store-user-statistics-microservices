import requests
from fastapi import APIRouter, Depends, status

from ..config import base_config
from ..dependencies import active_required, admin_required, pagination_query_params
from ..schemas import event_schemas

event_router = APIRouter()


@event_router.post("/", status_code=status.HTTP_201_CREATED)
def create_event_view(
    event: event_schemas.EventCreate, consumer=Depends(active_required)
):
    payload = event.dict()
    payload["store_id"] = consumer.id
    url = f"{base_config.EVENT_SERVICE_URL}/api/event/"
    return requests.post(url=url, json=payload).json()


@event_router.get(
    "/amount/{event_type}",
    dependencies=[Depends(active_required)],
    status_code=status.HTTP_200_OK,
)
def events_amount_view(
    event_type: str,
    query_params: dict = Depends(pagination_query_params),
):
    url = f"{base_config.EVENT_SERVICE_URL}/api/event/amount/{event_type}"
    return requests.get(url=url, params=query_params).json()


@event_router.get(
    "/avg-time/{event_type}",
    dependencies=[Depends(active_required)],
    status_code=status.HTTP_200_OK,
)
def events_avg_time_view(
    event_type: str,
    query_params: dict = Depends(pagination_query_params),
):
    url = f"{base_config.EVENT_SERVICE_URL}/api/event/avg-time/{event_type}"
    return requests.get(url=url, params=query_params).json()


@event_router.get(
    "/store-events-amount/{store_id}/",
    dependencies=[Depends(admin_required)],
    status_code=status.HTTP_200_OK,
)
def store_events_amount_view(
    store_id: int,
    query_params: dict = Depends(pagination_query_params),
):
    url = f"{base_config.EVENT_SERVICE_URL}/api/event/store-events-amount/{store_id}/"
    return requests.get(url=url, params=query_params).json()
