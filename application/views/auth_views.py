from flask_restx import Resource, Namespace
from flask import request
from marshmallow import ValidationError

from api.parsers import auth_post, auth_put
from container import auth_service
from helpers.schemas import AuthPostSchema, AuthPutSchema

auth_ns = Namespace('auth', "Страница для авторизации пользователя")


@auth_ns.route('/')
class AuthsViews(Resource):
    @auth_ns.expect(auth_post)
    @auth_ns.response(200, 'OK')
    @auth_ns.response(400, 'BadRequest')
    def post(self):
        """ Создание токена для пользователя """
        data: dict = request.json

        try:
            AuthPostSchema().load(data)
        except ValidationError as e:
            return e.messages, 400

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

        try:
            AuthPutSchema().load(data)
        except ValidationError as e:
            return e.messages, 400

        refresh_token = data.get('refresh_token')
        tokens = auth_service.approve_refresh_token(refresh_token)
        return tokens, 200
