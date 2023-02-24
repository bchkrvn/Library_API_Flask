from flask_restx import Namespace, Resource
from flask import request, abort

from container import news_service, comment_service
from dao.models.models_dao import NewsSchema, CommentSchema
from helpers.decorators import auth_required

news_ns = Namespace('news')
news_schema = NewsSchema()
newss_schema = NewsSchema(many=True)
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


@news_ns.route('/')
class NewsViews(Resource):
    @auth_required
    def get(self):
        news = news_service.get_all()
        return newss_schema.dump(news), 200

    @auth_required
    def post(self):
        data = request.json
        if not data:
            abort(400)

        news_service.create(data)

        return '', 201


@news_ns.route('/<int:n_id>')
class NewssViews(Resource):
    @auth_required
    def get(self, n_id):
        news = news_service.get_one(n_id)
        news_dict = news_schema.dump(news)
        comments = comment_service.get_by_news_id(n_id)
        comments_list = comments_schema.dump(comments)
        news_dict['comments'] = comments_list

        return news_dict, 200

    @auth_required
    def post(self, n_id):
        data = request.json
        if not data:
            abort(400)

        data['news_id'] = n_id
        comment_service.create(data)

        return '', 201

    @auth_required
    def put(self, n_id):
        data = request.json
        if not data:
            abort(400)

        data['id'] = n_id
        news_service.update(data)

        return '', 204

    @auth_required
    def delete(self, n_id):
        news_service.delete(n_id)
        return '', 204
