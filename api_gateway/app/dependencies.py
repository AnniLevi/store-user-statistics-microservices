from fastapi import Depends
from sqlalchemy.orm import Session

from .config.db_config import SessionLocal
from .db_crud.auth_db import get_consumer_by_name
from .models import Consumer
from .utils.exc import exceptions
from .utils.jwt import oauth2_scheme, parse_token


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def pagination_query_params(offset: int = 0, limit: int = 50):
    return {"offset": offset, "limit": limit}


def _get_current_consumer(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """by jwt token."""
    token_data = parse_token(token=token)
    consumer = get_consumer_by_name(db=db, name=token_data.name)
    if not consumer:
        raise exceptions["credentials_exc"]
    return consumer


def active_required(consumer: Consumer = Depends(_get_current_consumer)):
    if not consumer.is_active:
        raise exceptions["inactive_exc"]
    return consumer


def admin_required(consumer: Consumer = Depends(_get_current_consumer)):
    if not consumer.is_admin:
        raise exceptions["not_found_exc"]
    return consumer
