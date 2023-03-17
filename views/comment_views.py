from flask_restx import Namespace, Resource
from flask import request, abort

from api.parsers import comments_parser
from container import comment_service
from helpers.decorators import user_required

comment_ns = Namespace('comments', 'Страница для работы с комментариями')


@comment_ns.route('/<int:c_id>')
class CommentView(Resource):
    @comment_ns.expect(comments_parser)
    @comment_ns.response(204, 'NoContent')
    @comment_ns.response(400, 'BadRequest')
    @comment_ns.response(401, 'Unauthorized')
    @comment_ns.response(404, 'NotFound')
    @user_required
    def put(self, c_id, u_id):
        """Страница для изменения комментария"""
        data = request.json

        if not data:
            abort(400, "Data didn't send")
        elif 'text' not in data:
            abort(400, "Wrong key")
        elif data['text'] is None or '':
            abort(400, "Text didn't send")

        data['id'] = c_id
        data['user_id'] = u_id
        comment_service.update(data)

        return '', 204

    @comment_ns.response(204, 'NoContent')
    @comment_ns.response(400, 'BadRequest')
    @comment_ns.response(401, 'Unauthorized')
    @comment_ns.response(404, 'NotFound')
    @user_required
    def delete(self, c_id, u_id):
        """Страница для удаления комментария"""
        comment_service.delete(c_id, u_id)
        return '', 204
