from flask_restx import Resource, Namespace
from flask import request, abort

from container import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthsViews(Resource):
    def post(self):
        """ Создание токена для пользователя """
        data = request.json
        if not data:
            abort(400, "Data didn't send")
        username = data.get('username')
        password = data.get('password')

        if None in [username, password]:
            abort(400, 'username or password is None')

        tokens = auth_service.generate_token(username, password)

        return tokens, 200

    def put(self):
        """ Обновление токена пользователя """
        data = request.json
        if not data:
            abort(400)
        refresh_token = data.get('refresh_token')

        if not refresh_token:
            abort(400)

        tokens = auth_service.approve_refresh_token(refresh_token)
        return tokens
