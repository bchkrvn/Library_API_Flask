from flask_restx import Resource, Namespace
from flask import request, abort

from container import books_service
from dao.models_dao import BookSchema
from helpers.decorators import admin_required, auth_required

book_ns = Namespace('/books')
book_schema = BookSchema()
books_schema = BookSchema(many=True)


@book_ns.route('/')
class BooksViews(Resource):
    @auth_required
    def get(self):
        section = request.values.get('section')
        author_id = request.values.get('author_id')
        reader_id = request.values.get('reader_id')
        books = books_service.filter_books(author_id, reader_id, section)
        return books_schema.dump(books), 200

    @admin_required
    def post(self):
        data = request.json
        if not data:
            abort(400)
        books_service.create(data)
        return '', 201


@book_ns.route('/<int:id_>')
class BookViews(Resource):
    @auth_required
    def get(self, id_):
        book = books_service.get_one(id_)
        return book_schema.dump(book), 200

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
