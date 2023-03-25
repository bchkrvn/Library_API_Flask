from flask_restx import Resource, Namespace
from flask import request, abort

from api.models import user
from api.parsers import user_post_register, user_post_password, user_put
from container import user_service
from helpers.decorators import admin_required, user_required

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

        if not user_data:
            abort(400, "data didn't send")
        elif {'username'} != set(user_data.keys()):
            abort(400, 'wrong key')
        elif user_data['username'] in [None, '']:
            abort(400, "wrong value")

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

        if not user_data:
            abort(400, "data didn't send")
        elif {'username'} != set(user_data.keys()):
            abort(400, 'wrong key')
        elif user_data['username'] in [None, '']:
            abort(400, "wrong value")

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

        if not data:
            abort(400, 'Data did not send')
        elif set(data.keys()) != {'username', 'password'}:
            abort(400, 'Wrong key')
        values = data.values()
        if None in values or '' in values:
            abort(400, 'Wrong values')

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

        if not passwords:
            abort(400, 'Data did not send')
        elif not set(passwords.keys()) <= {'old_password', 'new_password'}:
            abort(400, 'Wrong key')
        values = passwords.values()
        if None in values or '' in values:
            abort(400, 'Wrong values')

        passwords['user_id'] = u_id
        user_service.change_password(passwords)
        return '', 204
