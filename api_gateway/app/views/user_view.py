import requests
from fastapi import APIRouter, Depends, status

from ..config import base_config
from ..dependencies import active_required
from ..models import Consumer
from ..schemas import user_schemas

user_router = APIRouter()


@user_router.get(
    "/{email}", dependencies=[Depends(active_required)], status_code=status.HTTP_200_OK
)
def get_user_id_by_email(email=str):
    url = f"{base_config.USER_SERVICE_URL}/api/user/{email}"
    return requests.get(url=url).json()


def _user_create_update_common(
    user: user_schemas.UserCreate, consumer=Consumer
) -> tuple[str, dict]:
    payload = user.dict()
    payload["store_id"] = consumer.id
    url = f"{base_config.USER_SERVICE_URL}/api/user/"
    return url, payload


@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: user_schemas.UserCreate, consumer=Depends(active_required)):
    url, payload = _user_create_update_common(user, consumer)
    return requests.post(url=url, data=payload).json()


@user_router.patch("/", status_code=status.HTTP_201_CREATED)
def update_user(user: user_schemas.UserCreate, consumer=Depends(active_required)):
    url, payload = _user_create_update_common(user, consumer)
    return requests.patch(url=url, data=payload).json()


@user_router.delete(
    "/{user_id}", dependencies=[Depends(active_required)], status_code=status.HTTP_200_OK
)
def delete_user_events(user_id: str):
    user_url = f"{base_config.USER_SERVICE_URL}/api/user/{user_id}"
    event_url = f"{base_config.EVENT_SERVICE_URL}/api/event/{user_id}"
    user_response = requests.delete(url=user_url).json()
    event_response = requests.delete(url=event_url).json()
    return {"user": user_response["message"], "events": event_response["message"]}
