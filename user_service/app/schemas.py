from . import ma
from .models import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone",
            "store_id",
        )
        load_instance = True
        # sqla_session = db.session


class UserIdSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ("id",)
        load_instance = True
