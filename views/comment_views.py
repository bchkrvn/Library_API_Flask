from flask_restx import Namespace, Resource
from flask import request, abort

from container import comment_service
from helpers.decorators import auth_required, user_required

comment_ns = Namespace('comments')


@comment_ns.route('/<int:c_id>')
class CommentView(Resource):
    @user_required
    def put(self, c_id, u_id):
        data = request.json
        if not data:
            abort(400)

        data['id'] = c_id
        data['user_id'] = u_id
        comment_service.update(data)

        return '', 204

    @user_required
    def delete(self, c_id, u_id):
        comment_service.delete(c_id, u_id)
        return '', 204
