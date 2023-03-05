from flask_restx import Resource, Namespace
from flask import request, abort

from container import user_service
from dao.models.models_dao import UserSchema
from helpers.decorators import admin_required, user_required

user_ns = Namespace('users', 'Страница для работы с пользователями')
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UsersViews(Resource):
    @user_required
    def get(self, u_id):
        user = user_service.get_one(u_id)
        return user_schema.dump(user), 200

    @user_required
    def put(self, u_id):
        user_data = request.json
        if not user_data:
            abort(400)
        user_data['id'] = u_id
        user_service.update(user_data)
        return '', 204

    @user_required
    def patch(self, u_id):
        user_data = request.json
        if not user_data:
            abort(400)
        user_data['id'] = u_id
        user_service.update_partial(user_data)
        return '', 204

    @user_required
    def delete(self, u_id):
        user_service.delete(u_id)
        return '', 204


@user_ns.route('/<int:u_id>')
class UserViews(Resource):

    @admin_required
    def get(self, u_id):
        """
        Получение информации о пользователе
        """
        user = user_service.get_one(u_id)
        return user_schema.dump(user), 200

    @admin_required
    def put(self, u_id):
        user_data = request.json
        if not user_data:
            abort(400)
        user_data['id'] = u_id
        user_service.update(user_data)
        return '', 204

    @admin_required
    def delete(self, u_id):
        user_service.delete(u_id)
        return '', 204


@user_ns.route('/all')
class UserAllViews(Resource):
    @admin_required
    def get(self, u_id):
        users = user_service.get_all()
        return users_schema.dump(users), 200


@user_ns.route('/register')
class UserRegisterView(Resource):
    def post(self):
        """
        Страница регистрации нового пользователя
        """
        user_data = request.json
        if not user_data:
            abort(400)
        user_service.create(user_data)
        return '', 201


@user_ns.route('/password')
class UserPasswordView(Resource):
    @user_required
    def post(self, u_id):
        passwords = request.json
        if ['old_password', 'new_password'] != list(passwords.keys()):
            abort(400)
        passwords['user_id'] = u_id
        user_service.change_password(passwords)
        return '', 204
