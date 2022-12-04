from fastapi import APIRouter

from .views import auth_view, store_view

api_router = APIRouter()

api_router.include_router(auth_view.auth_router, prefix="/auth")
api_router.include_router(store_view.store_router, prefix="/store")
