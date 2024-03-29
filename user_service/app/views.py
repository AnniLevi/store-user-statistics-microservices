from flask import Blueprint, make_response
from flask_restful import Api, Resource, abort, reqparse
from sqlalchemy import or_
from sqlalchemy.exc import NoResultFound

from . import db
from .models import User
from .schemas import UserIdSchema, UserSchema

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)


class AuthView(Resource):
    def post(self):
        parser = self._get_request_body_parser()
        parser.replace_argument("username", type=str, location="form", required=True)
        data = parser.parse_args()
        user = User.query.filter(
            or_(User.username.like(data["username"]), User.email.like(data["email"]))
        ).one_or_none()
        if user:
            abort(406, message=f"User with given username or email already exists")

        schema = UserSchema()
        new_user = schema.load(data, session=db.session)
        db.session.add(new_user)
        db.session.commit()
        return schema.dump(new_user), 201

    def patch(self):
        parser = self._get_request_body_parser()
        data = parser.parse_args()
        user = User.query.filter(User.email.like(data["email"])).one_or_none()

        if not user:
            abort(404, message="User with given email not found")

        user.username = data["username"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.phone = data["phone"]
        db.session.merge(user)
        db.session.commit()
        return make_response({"message": "User successfully updated"}, 201)

    def _get_request_body_parser(self) -> reqparse.RequestParser:
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, location="form", required=True)
        parser.add_argument("username", type=str, location="form")
        parser.add_argument("first_name", type=str, location="form")
        parser.add_argument("last_name", type=str, location="form")
        parser.add_argument("phone", type=int, location="form")
        parser.add_argument("store_id", type=int, location="form", required=True)
        return parser


class UserRetrieveView(Resource):
    def get(self, user_email: str):
        try:
            user = User.query.filter(User.email.like(user_email)).one()
            schema = UserIdSchema()
            return schema.dump(user)
        except NoResultFound:
            abort(404, message="User with given email not found")


class UserDeleteView(Resource):
    def delete(self, user_id: str):
        user = User.query.filter(User.id == user_id).one_or_none()
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return make_response({"message": "User successfully deleted"}, 200)


class UserDeleteByStoreView(Resource):
    def delete(self, store_id: int):
        users = User.query.filter(User.store_id == store_id).delete()
        if not users:
            abort(404, message="Users not found")
        db.session.commit()
        return make_response({"message": f"{users} users were deleted"}, 200)


api.add_resource(AuthView, "/user/")
api.add_resource(UserRetrieveView, "/user/<user_email>")
api.add_resource(UserDeleteView, "/user/<user_id>")
api.add_resource(UserDeleteByStoreView, "/user/by-store/<store_id>")
