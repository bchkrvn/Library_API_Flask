from flask_restx import Namespace, Resource
from flask import request, abort

from container import comment_service
from helpers.decorators import auth_required

comment_ns = Namespace('comments')


@comment_ns.route('/<int:id_>')
class CommentView(Resource):
    @auth_required
    def put(self, id_):
        data = request.json
        if not data:
            abort(400)

        data['id'] = id_
        comment_service.update(data)

        return '', 204

    @auth_required
    def delete(self, id_):
        comment_service.delete(id_)
        return '', 204
