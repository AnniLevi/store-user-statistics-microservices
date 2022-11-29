from fastapi import APIRouter

from . import views

api_router = APIRouter()

api_router.include_router(views.event_router, prefix="/event")
