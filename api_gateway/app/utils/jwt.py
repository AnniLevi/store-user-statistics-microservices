from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session

from ..config import base_config
from ..db_crud import auth_db
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


def authenticate_consumer(db: Session, api_key: str):
    """by api key."""
    consumer = auth_db.get_consumer_by_api_key(db=db, api_key=api_key)
    if not consumer:
        raise exceptions["apikey_exc"]
    access_token = create_access_token(data={"sub": consumer.name})
    return access_token
