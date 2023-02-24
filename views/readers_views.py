from flask_restx import Namespace, Resource
from flask import request, abort

from container import reader_service
from dao.models.models_dao import ReaderSchema
from helpers.decorators import admin_required, user_required

reader_ns = Namespace('readers')
reader_schema = ReaderSchema()
readers_schema = ReaderSchema(many=True)


@reader_ns.route('/')
class ReadersViews(Resource):
    @admin_required
    def get(self):
        readers = reader_service.get_all()
        return readers_schema.dump(readers), 200


@reader_ns.route('/<int:u_id>')
class ReaderViews(Resource):
    @user_required
    def get(self, u_id):
        reader = reader_service.get_one(u_id)
        return reader_schema.dump(reader)

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

