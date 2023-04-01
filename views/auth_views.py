from flask_restx import Resource, Namespace
from flask import request, abort
from marshmallow import ValidationError

from api.parsers import auth_post, auth_put
from container import auth_service
auth_ns = Namespace('auth', "Страница для авторизации пользователя")


@auth_ns.route('/')
class AuthsViews(Resource):
    @auth_ns.expect(auth_post)
    @auth_ns.response(200, 'OK')
    @auth_ns.response(400, 'BadRequest')
    def post(self):
        """ Создание токена для пользователя """
        data: dict = request.json

        if not data:
            abort(400, "Data didn't send")
        elif set(data.keys()) != {"username", "password"}:
            abort(400, "Wrong keys")
        elif None in data.values() or '' in data.values():
            abort(400, "Wrong keys")
        # try:
        #     UserRegisterSchema().load(data)
        # except ValidationError as e:
        #     abort(400, f'{e.messages}')

        username = data.get('username')
        password = data.get('password')

        tokens = auth_service.generate_token(username, password)
        return tokens, 200

    @auth_ns.expect(auth_put)
    @auth_ns.response(200, 'OK')
    @auth_ns.response(400, 'BadRequest')
    def put(self):
        """ Обновление токена пользователя """
        data: dict = request.json

        if not data:
            abort(400, "Data didn't send")
        elif {'refresh_token', } != set(data.keys()):
            abort(400, 'Wrong keys')
        elif data.get('refresh_token') in [None, '']:
            abort(400, 'Wrong values')

        refresh_token = data.get('refresh_token')
        tokens = auth_service.approve_refresh_token(refresh_token)
        return tokens, 200
