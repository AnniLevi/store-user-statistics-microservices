import requests
from fastapi import APIRouter, Depends, status

from ..config import base_config
from ..dependencies import active_required
from ..schemas import user_schemas

user_router = APIRouter()


@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: user_schemas.UserCreate, consumer=Depends(active_required)):
    payload = user.dict()
    payload["store_id"] = consumer.id
    url = f"{base_config.USER_SERVICE_URL}/api/user/"
    return requests.post(url=url, data=payload).json()
