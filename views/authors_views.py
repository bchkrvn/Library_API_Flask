from flask_restx import Resource, Namespace
from flask import request, abort

from api.models import author
from container import author_service
from dao.models.models_dao import AuthorSchema
from helpers.decorators import admin_required, auth_required

author_ns = Namespace('authors')
author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)


@author_ns.route('/')
class AuthorsViews(Resource):
    @author_ns.marshal_with(author, as_list=True, code=200, description='OK')
    @auth_required
    def get(self):
        return author_service.get_all()

    @admin_required
    def post(self):
        data = request.json
        if not data:
            abort(400)
        author_service.create(data)
        return '', 201


@author_ns.route('/<int:id_>')
class AuthorViews(Resource):
    @author_ns.marshal_with(author, as_list=False, code=200, description='OK')
    @auth_required
    def get(self, id_):
        return author_service.get_one(id_)

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
