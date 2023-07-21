from flask_restx import Resource, Namespace
from flask import request, abort
from marshmallow import ValidationError

from ..api.models import user
from ..api.parsers import user_post_register, user_post_password, user_put
from ..container import user_service
from ..helpers.decorators import admin_required, user_required
from ..helpers.schemas.user_schemas import UserSchema, UserPasswordSchema

user_ns = Namespace('users', 'Страница для работы с пользователями')


@user_ns.route('/')
class UsersViews(Resource):
    @user_ns.marshal_with(user, as_list=False, code=200, description='OK')
    @user_ns.response(401, 'Unauthorized')
    @user_required
    def get(self, u_id):
        """
        Получить информацию о пользователе, доступно только пользователю
        """
        return user_service.get_one(u_id)

    @user_ns.expect(user_put)
    @user_ns.response(400, 'BadRequest')
    @user_ns.response(204, 'NoContent')
    @user_ns.response(401, 'Unauthorized')
    @user_required
    def put(self, u_id):
        """
        Обновить информацию о пользователе, доступно только пользователю
        """
        user_data = request.json

        try:
            UserSchema().load(user_data, partial=("password",))
        except ValidationError:
            abort(400, f'Wrong data')

        user_data['id'] = u_id
        user_service.update(user_data)
        return '', 204

    @user_ns.response(204, 'NoContent')
    @user_ns.response(401, 'Unauthorized')
    @user_required
    def delete(self, u_id):
        """
        Удалить пользователя, доступно только пользователю
        """
        user_service.delete(u_id)
        return '', 204


@user_ns.route('/<int:u_id>')
class UserViews(Resource):
    @user_ns.response(404, 'NotFound')
    @user_ns.marshal_with(user, as_list=False, code=200, description='OK')
    @admin_required
    def get(self, u_id):
        """
        Получение информации о пользователе, доступно администратору
        """
        return user_service.get_one(u_id)

    @user_ns.response(404, 'NotFound')
    @user_ns.response(400, 'BadRequest')
    @user_ns.response(204, 'NoContent')
    @user_ns.response(401, 'Unauthorized')
    @user_ns.response(403, 'Forbidden')
    @user_ns.expect(user_put)
    @admin_required
    def put(self, u_id):
        """
        Обновление информации о пользователе, доступно администратору
        """
        user_data = request.json

        try:
            UserSchema().load(user_data, partial=("password",))
        except ValidationError:
            abort(400, f'Wrong data')

        user_data['id'] = u_id
        user_service.update(user_data)
        return '', 204

    @user_ns.response(404, 'NotFound')
    @user_ns.response(204, 'NoContent')
    @user_ns.response(401, 'Unauthorized')
    @user_ns.response(403, 'Forbidden')
    @admin_required
    def delete(self, u_id):
        """
        Удаление пользователя, доступно администратору
        """
        user_service.delete(u_id)
        return '', 204


@user_ns.route('/all')
class UserAllViews(Resource):
    @user_ns.response(401, 'Unauthorized')
    @user_ns.response(403, 'Forbidden')
    @user_ns.marshal_with(user, as_list=True, code=200, description='OK')
    @admin_required
    def get(self):
        """
        Получение всех пользователей, доступно администратору
        """
        return user_service.get_all()


@user_ns.route('/register')
class UserRegisterView(Resource):
    @user_ns.response(201, 'Created')
    @user_ns.response(400, 'BadRequest')
    @user_ns.expect(user_post_register)
    def post(self):
        """
        Страница регистрации нового пользователя
        """
        data = request.json

        try:
            UserSchema().load(data)
        except ValidationError:
            abort(400, f'Wrong data')

        user_service.create(data)
        return '', 201


@user_ns.route('/password')
class UserPasswordView(Resource):

    @user_ns.response(204, 'NoContent')
    @user_ns.response(400, 'BadRequest')
    @user_ns.response(401, 'Unauthorized')
    @user_ns.response(404, 'NotFound')
    @user_ns.expect(user_post_password)
    @user_required
    def post(self, u_id):
        """
        Страница для смены пароля пользователя
        """
        passwords = request.json

        try:
            UserPasswordSchema().load(passwords)
        except ValidationError:
            abort(400, f'Wrong data')

        passwords['user_id'] = u_id
        user_service.change_password(passwords)
        return '', 204
