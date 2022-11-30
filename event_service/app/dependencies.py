from .config.db_config import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def pagination_query_params(offset: int = 0, limit: int = 50):
    return {"offset": offset, "limit": limit}
