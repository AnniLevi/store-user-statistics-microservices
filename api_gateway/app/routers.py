from fastapi import APIRouter

from .views import auth_view, event_view, store_view, user_view

api_router = APIRouter()

api_router.include_router(auth_view.auth_router, prefix="/auth")
api_router.include_router(store_view.store_router, prefix="/store")
api_router.include_router(user_view.user_router, prefix="/user")
api_router.include_router(event_view.event_router, prefix="/event")
