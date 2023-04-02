from flask_restx import Namespace, Resource
from flask import request, abort
from marshmallow import ValidationError

from api.models import news
from api.parsers import news_parser
from container import news_service, comment_service
from dao.models.models_dao import NewsSchema, CommentSchema
from helpers.decorators import auth_required, user_required
from helpers.schemas.news_schema import NewsValidateSchema

news_ns = Namespace('news', 'Страница для получения новостей')
# comments_schema = CommentSchema(many=True)


@news_ns.route('/')
class NewsViews(Resource):

    @news_ns.response(401, 'Unauthorized')
    @news_ns.marshal_with(news, as_list=True, code=200, description='OK')
    @auth_required
    def get(self):
        """ Страница для получения всех новостей """
        news_ = news_service.get_all()
        news_list = NewsSchema(many=True).dump(news_)
        for news_ in news_list:
            news_['comments'] = comment_service.get_by_news_id(news_['id'])

        return news_list

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
        except ValidationError as e:
            abort(400, f'{e.messages}')

        data['user_id'] = u_id
        news_service.create(data)
        return '', 201


@news_ns.route('/<int:n_id>')
class OneNewsViews(Resource):
    @news_ns.response(200, 'OK')
    @news_ns.response(401, 'Unauthorized')
    @news_ns.response(404, 'NotFound')
    @news_ns.marshal_with(news, as_list=False, code=200, description='OK')
    @auth_required
    def get(self, n_id):
        """ Страница для получения новости с комментариями """
        news_ = news_service.get_one(n_id)
        news_dict = NewsSchema().dump(news_)
        comments = comment_service.get_by_news_id(n_id)
        news_dict['comments'] = comments

        return news_dict, 200

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
            NewsValidateSchema().load(data)
        except ValidationError as e:
            abort(400, f'{e.messages}')

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
        except ValidationError as e:
            abort(400, f'{e.messages}')

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
