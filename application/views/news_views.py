from flask_restx import Namespace, Resource
from flask import request, abort
from marshmallow import ValidationError

from api.models import news
from api.parsers import news_parser
from container import news_service, comment_service
from helpers.decorators import auth_required, user_required
from helpers.schemas.comments_schema import CommentsSchema
from helpers.schemas.news_schema import NewsValidateSchema

news_ns = Namespace('news', 'Страница для получения новостей')


@news_ns.route('/')
class NewsViews(Resource):

    @news_ns.response(401, 'Unauthorized')
    @news_ns.marshal_with(news, as_list=True, code=200, description='OK')
    @auth_required
    def get(self):
        """ Страница для получения всех новостей """
        news_ = news_service.get_all()
        return news_

    @news_ns.expect(news_parser)
    @news_ns.response(201, 'Created')
    @news_ns.response(400, 'BadRequest')
    @news_ns.response(401, 'Unauthorized')
    @news_ns.response(403, 'Forbidden')
    @news_ns.response(404, 'NotFound')
    @user_required
    def post(self, u_id):
        """ Страница для публикации новой новости """
        data = request.json

        try:
            NewsValidateSchema().load(data)
        except ValidationError:
            abort(400, f'Wrong data')

        data['user_id'] = u_id
        news_service.create(data)
        return '', 201


@news_ns.route('/<int:n_id>/')
class OneNewsViews(Resource):
    @news_ns.response(200, 'OK')
    @news_ns.response(401, 'Unauthorized')
    @news_ns.response(404, 'NotFound')
    @news_ns.marshal_with(news, as_list=False, code=200, description='OK')
    @auth_required
    def get(self, n_id):
        """ Страница для получения новости с комментариями """
        news_ = news_service.get_one(n_id)

        return news_, 200

    @news_ns.expect(news_parser)
    @news_ns.response(201, 'Created')
    @news_ns.response(400, 'BadRequest')
    @news_ns.response(401, 'Unauthorized')
    @news_ns.response(404, 'NotFound')
    @user_required
    def post(self, n_id, u_id):
        """Страница для публикации нового комментария"""
        data = request.json

        try:
            CommentsSchema().load(data)
        except ValidationError:
            abort(400, f'Wrong data')

        data['news_id'] = n_id
        data['user_id'] = u_id
        comment_service.create(data)

        return '', 201

    @news_ns.expect(news_parser)
    @news_ns.response(204, 'NoContent')
    @news_ns.response(400, 'BadRequest')
    @news_ns.response(401, 'Unauthorized')
    @news_ns.response(403, 'Forbidden')
    @news_ns.response(404, 'NotFound')
    @user_required
    def put(self, n_id, u_id):
        """ Страница для редактирования новости"""
        data = request.json
        try:
            NewsValidateSchema().load(data)
        except ValidationError:
            abort(400, f'Wrong data')

        data['n_id'] = n_id
        data['u_id'] = u_id
        news_service.update(data)
        return '', 204

    @news_ns.expect(news_parser)
    @news_ns.response(204, 'NoContent')
    @news_ns.response(400, 'BadRequest')
    @news_ns.response(401, 'Unauthorized')
    @news_ns.response(404, 'NotFound')
    @user_required
    def delete(self, n_id, u_id):
        """Страница для удаления новости"""
        news_service.delete(n_id, u_id)
        return '', 204
