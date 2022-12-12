from sqlalchemy.orm import Session

from ..models import ApiKey, Consumer


def get_consumer_by_api_key(db: Session, api_key: str):
    return db.query(Consumer).join(ApiKey).filter(ApiKey.key == api_key).first()


def get_consumer_by_name(db: Session, name: str):
    return db.query(Consumer).filter(Consumer.name == name).first()
