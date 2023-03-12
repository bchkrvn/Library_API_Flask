from flask_restx import Namespace, Resource
from flask import request, abort

from api.models import reader
from container import reader_service
from dao.models.models_dao import ReaderSchema
from helpers.decorators import admin_required, user_required

reader_ns = Namespace('readers')
reader_schema = ReaderSchema()
readers_schema = ReaderSchema(many=True)


@reader_ns.route('/')
class ReadersViews(Resource):
    @reader_ns.marshal_with(reader, as_list=True, code=200, description='OK')
    @user_required
    def get(self, u_id):
        return reader_service.get_one(u_id)

    @user_required
    def put(self, u_id):
        data = request.json
        if not data:
            abort(400)
        data['id'] = u_id
        reader_service.update(data)
        return '', 204

    @user_required
    def patch(self, u_id):
        data = request.json
        if not data:
            abort(400)
        data['id'] = u_id
        reader_service.update_partial(data)
        return '', 204


@reader_ns.route('/<int:u_id>')
class ReaderViews(Resource):
    @reader_ns.marshal_with(reader, code=200, description='OK')
    @admin_required
    def get(self, u_id):
        return reader_service.get_one(u_id)

    @admin_required
    def put(self, u_id):
        data = request.json
        if not data:
            abort(400)
        data['id'] = u_id
        reader_service.update(data)
        return '', 204

    @admin_required
    def patch(self, u_id):
        data = request.json
        if not data:
            abort(400)
        data['id'] = u_id
        reader_service.update_partial(data)
        return '', 204


@reader_ns.route('/all')
class ReadersViews(Resource):
    @reader_ns.marshal_with(reader, as_list=True, code=200, description='OK')
    @admin_required
    def get(self):
        readers = reader_service.get_all()
        return readers
