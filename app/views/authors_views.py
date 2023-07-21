from flask_restx import Resource, Namespace
from flask import request, abort
from marshmallow import ValidationError

from app.api.models import author
from app.api.parsers import author_patch, author_post_put
from app.container import author_service
from app.helpers.decorators import admin_required, auth_required
from app.helpers.schemas.authors_schemas import AuthorSchema

author_ns = Namespace('authors', "Страница для работы с авторами")


@author_ns.route('/')
class AuthorsViews(Resource):
    @author_ns.response(401, 'Unauthorized')
    @author_ns.marshal_with(author, as_list=True, code=200, description='OK')
    @auth_required
    def get(self):
        """Страница для получения всех авторов, доступна авторизованным пользователям"""
        return author_service.get_all()

    @author_ns.expect(author_post_put)
    @author_ns.response(201, 'Created')
    @author_ns.response(400, 'BadRequest')
    @author_ns.response(401, 'Unauthorized')
    @author_ns.response(403, 'Forbidden')
    @admin_required
    def post(self):
        """Страница для добавления нового автора, доступна администратору"""
        data: dict = request.json

        try:
            AuthorSchema().load(data)
        except ValidationError:
            abort(400, 'Wrong data')

        author_service.create(data)
        return '', 201


@author_ns.route('/<int:id_>')
class AuthorViews(Resource):
    @author_ns.response(401, 'Unauthorized')
    @author_ns.response(404, 'NotFound')
    @author_ns.marshal_with(author, as_list=False, code=200, description='OK')
    @auth_required
    def get(self, id_):
        """Страница для получения информации об одном авторе, доступна авторизованным пользователям"""
        return author_service.get_one(id_)

    @author_ns.expect(author_post_put)
    @author_ns.response(204, 'NoContent')
    @author_ns.response(400, 'BadRequest')
    @author_ns.response(401, 'Unauthorized')
    @author_ns.response(403, 'Forbidden')
    @author_ns.response(404, 'NotFound')
    @admin_required
    def put(self, id_):
        """Страница для изменения автора, доступна администратору"""
        data = request.json

        try:
            AuthorSchema().load(data)
        except ValidationError:
            abort(400, 'Wrong data')

        data['id'] = id_
        author_service.update(data)
        return '', 204

    @author_ns.expect(author_patch)
    @author_ns.response(204, 'NoContent')
    @author_ns.response(400, 'BadRequest')
    @author_ns.response(401, 'Unauthorized')
    @author_ns.response(403, 'Forbidden')
    @author_ns.response(404, 'NotFound')
    @admin_required
    def patch(self, id_):
        """Страница для частичного изменения автора, доступна администратору"""
        data = request.json

        try:
            AuthorSchema(partial=True).load(data)
        except ValidationError:
            abort(400, 'Wrong data')

        data['id'] = id_
        author_service.update_partial(data)
        return '', 204

    @author_ns.response(204, 'NoContent')
    @author_ns.response(400, 'BadRequest')
    @author_ns.response(401, 'Unauthorized')
    @author_ns.response(404, 'NotFound')
    @admin_required
    def delete(self, id_):
        """Страница для удаления автора, доступна администратору"""
        author_service.delete(id_)
        return '', 204
