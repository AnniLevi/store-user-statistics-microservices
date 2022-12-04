from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session

from ..config import base_config
from ..db_crud import auth_db
from ..dependencies import get_db
from ..models import Consumer
from ..schemas import auth_schemas
from .exc import exceptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=int(base_config.ACCESS_TOKEN_EXPIRE_MINUTES))
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, base_config.JWT_SECRET_KEY, algorithm=base_config.ALGORITHM
    )
    return encoded_jwt


def parse_token(token: str):
    try:
        payload = jwt.decode(
            token, base_config.JWT_SECRET_KEY, algorithms=[base_config.ALGORITHM]
        )
        name: str = payload.get("sub")
        if name is None:
            raise exceptions["credentials_exc"]
        token_data = auth_schemas.TokenData(name=name)
        return token_data
    except ExpiredSignatureError:
        raise exceptions["expire_exc"]
    except JWTError:
        raise exceptions["credentials_exc"]


def get_current_consumer(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """by jwt token."""
    token_data = parse_token(token=token)
    consumer = auth_db.get_consumer_by_name(db=db, name=token_data.name)
    if not consumer:
        raise exceptions["credentials_exc"]
    return consumer


def authenticate_consumer(db: Session, api_key: str):
    """by api key."""
    consumer = auth_db.get_consumer_by_api_key(db=db, api_key=api_key)
    if not consumer:
        raise exceptions["apikey_exc"]
    access_token = create_access_token(data={"sub": consumer.name})
    return access_token


def active_required(consumer: Consumer = Depends(get_current_consumer)):
    if not consumer.is_active:
        raise exceptions["inactive_exc"]
    return consumer


def admin_required(consumer: Consumer = Depends(get_current_consumer)):
    if not consumer.is_admin:
        raise exceptions["admin_exc"]
    return consumer
