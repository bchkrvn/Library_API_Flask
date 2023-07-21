from flask_restx import Namespace, Resource
from flask import request, abort
from marshmallow import ValidationError

from ..api.models import reader
from ..api.parsers import reader_put, reader_patch
from ..container import reader_service
from ..helpers.decorators import admin_required, user_required
from ..helpers.schemas.readers_schemas import ReaderSchema

reader_ns = Namespace('readers', "Страница для работы с читателями")


@reader_ns.route('/')
class ReadersViews(Resource):
    @reader_ns.response(401, 'Unauthorized')
    @reader_ns.marshal_with(reader, as_list=True, code=200, description='OK')
    @user_required
    def get(self, u_id):
        """Страница для получения информации о читателе, доступно пользователю"""
        return reader_service.get_one(u_id)

    @reader_ns.expect(reader_put)
    @reader_ns.response(400, 'BadRequest')
    @reader_ns.response(401, 'Unauthorized')
    @user_required
    def put(self, u_id):
        """Страница для редактирования информации о читателе"""
        data = request.json

        try:
            ReaderSchema().load(data)
        except ValidationError:
            abort(400, 'Wrong data')

        data['id'] = u_id
        reader_service.update(data)
        return '', 204

    @reader_ns.expect(reader_patch)
    @reader_ns.response(400, 'BadRequest')
    @reader_ns.response(401, 'Unauthorized')
    @user_required
    def patch(self, u_id):
        """Страница для частичного редактирования информации о читателе, доступно пользователю"""
        data = request.json

        try:
            ReaderSchema(partial=True).load(data)
        except ValidationError:
            abort(400, 'Wrong data')

        data['id'] = u_id
        reader_service.update_partial(data)
        return '', 204


@reader_ns.route('/<int:u_id>')
class ReaderViews(Resource):

    @reader_ns.response(401, 'Unauthorized')
    @reader_ns.response(404, 'NotFound')
    @reader_ns.marshal_with(reader, code=200, description='OK')
    @admin_required
    def get(self, u_id):
        """Страница для получения информации о читателе, доступно администратору"""

        return reader_service.get_one(u_id)

    @reader_ns.expect(reader_put)
    @reader_ns.response(400, 'BadRequest')
    @reader_ns.response(401, 'Unauthorized')
    @reader_ns.response(404, 'NotFound')
    @admin_required
    def put(self, u_id):
        """Страница для обновления информации о читателе, доступно администратору"""

        data = request.json
        try:
            ReaderSchema().load(data)
        except ValidationError:
            abort(400, 'Wrong data')

        data['id'] = u_id
        reader_service.update(data)
        return '', 204

    @reader_ns.expect(reader_patch)
    @reader_ns.response(400, 'BadRequest')
    @reader_ns.response(401, 'Unauthorized')
    @reader_ns.response(404, 'NotFound')
    @admin_required
    def patch(self, u_id):
        """Страница для частичного обновления информации о читателе, доступно администратору"""

        data = request.json
        try:
            ReaderSchema(partial=True).load(data)
        except ValidationError:
            abort(400, 'Wrong data')

        data['id'] = u_id
        reader_service.update_partial(data)
        return '', 204


@reader_ns.route('/all')
class ReadersViews(Resource):
    @reader_ns.marshal_with(reader, as_list=True, code=200, description='OK')
    @reader_ns.response(400, 'BadRequest')
    @reader_ns.response(401, 'Unauthorized')
    @reader_ns.response(404, 'NotFound')
    @admin_required
    def get(self):
        """Страница для получения информации о всех читателях, доступно администратору"""

        return reader_service.get_all()
