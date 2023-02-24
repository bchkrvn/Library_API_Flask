from flask_restx import Resource, Namespace
from flask import request, abort

from container import author_service
from dao.models.models_dao import AuthorSchema
from helpers.decorators import admin_required, auth_required

author_ns = Namespace('authors')
author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)


@author_ns.route('/')
class AuthorsViews(Resource):
    @auth_required
    def get(self):
        authors = author_service.get_all()
        return authors_schema.dump(authors), 200

    @admin_required
    def post(self):
        data = request.json
        if not data:
            abort(400)
        author_service.create(data)
        return '', 201


@author_ns.route('/<int:id_>')
class AuthorViews(Resource):
    @auth_required
    def get(self, id_):
        author = author_service.get_one(id_)
        return author_schema.dump(author), 200

    @admin_required
    def put(self, id_):
        data = request.json
        if not data:
            abort(400)
        data['id'] = id_
        author_service.update(data)
        return '', 204

    @admin_required
    def patch(self, id_):
        data = request.json
        if not data:
            abort(400)
        data['id'] = id_
        author_service.update_partial(data)
        return '', 204

    @admin_required
    def delete(self, id_):
        author_service.delete(id_)
        return '', 204
