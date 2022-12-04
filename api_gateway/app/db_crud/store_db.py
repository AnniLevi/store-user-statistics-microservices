from sqlalchemy.orm import Session

from ..models import Consumer


def all_stores_db(db: Session, offset: int, limit: int):
    return (
        db.query(Consumer).filter_by(is_admin=False).offset(offset).limit(limit).all()
    )
