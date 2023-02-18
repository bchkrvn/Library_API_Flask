from flask_restx import Resource, Namespace
from flask import request

from container import user_service
from dao.models_dao import UserSchema
from helpers.decorators import admin_required, user_required

user_ns = Namespace('users')
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UsersViews(Resource):
    @admin_required
    def get(self):
        users = user_service.get_all()
        return users_schema.dump(users), 200

    def post(self):
        user_data = request.json
        user_service.create(user_data)
        return '', 201


@user_ns.route('/<int:u_id>')
class UserViews(Resource):
    @user_required
    def get(self, u_id):
        user = user_service.get_one(u_id)
        return user_schema.dump(user), 200

    @user_required
    def put(self, u_id):
        user_data = request.json
        user_data['id'] = u_id
        user_service.update(user_data)
        return '', 204

    @user_required
    def patch(self, u_id):
        user_data = request.json
        user_data['id'] = u_id
        user_service.update_partial(user_data)
        return '', 204

    @user_required
    def delete(self, u_id):
        user_service.delete(u_id)
        return '', 204
