from flask_restx import Resource, Namespace
from flask import request, abort

from api.models import book
from api.parsers import books_get, books_post
from container import books_service
from dao.models.models_dao import BookSchema
from helpers.decorators import admin_required, auth_required

book_ns = Namespace('books')
book_schema = BookSchema()
books_schema = BookSchema(many=True)


@book_ns.route('/')
class BooksViews(Resource):
    @book_ns.expect(books_get)
    @book_ns.marshal_with(book, as_list=True, code=200, description='OK')
    @auth_required
    def get(self):
        books = books_service.filter_books(**books_get.parse_args())
        return books

    @book_ns.expect(books_post)
    @admin_required
    def post(self):
        data = request.json
        if not data:
            abort(400)
        books_service.create(data)
        return '', 201


@book_ns.route('/<int:id_>')
class BookViews(Resource):
    @book_ns.marshal_with(book, code=200, description='OK')
    @auth_required
    def get(self, id_):
        return books_service.get_one(id_)

    @admin_required
    def put(self, id_):
        data = request.json
        if not data:
            abort(400)
        data['id'] = id_
        books_service.update(data)
        return '', 204

    @admin_required
    def patch(self, id_):
        data = request.json
        if not data:
            abort(400)
        data['id'] = id_
        books_service.update_partial(data)
        return '', 204

    @admin_required
    def delete(self, id_):
        books_service.delete(id_)
        return '', 204


@book_ns.route('/give')
class BookGiveViews(Resource):
    @admin_required
    def post(self):
        data = request.json
        if not data:
            abort(400)
        if ['reader_id', 'book_id'] == data.keys():
            abort(400)
        books_service.give_book_to_reader(data)
        return '', 204


@book_ns.route('/get')
class BookGetViews(Resource):
    @admin_required
    def post(self):
        data = request.json
        if not data:
            abort(400)
        if 'book_id' == data.keys():
            abort(400)
        books_service.get_book_from_reader(data)
        return '', 204
