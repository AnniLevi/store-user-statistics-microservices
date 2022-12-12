import uuid

from sqlalchemy.dialects.postgresql import UUID

from . import db


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    first_name = db.Column(db.String(300))
    last_name = db.Column(db.String(300))
    phone = db.Column(db.Integer)
    store_id = db.Column(db.Integer)
