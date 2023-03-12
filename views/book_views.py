from flask_restx import Resource, Namespace
from flask import request, abort

from api.models import book
from api.parsers import books_get, books_post, books_put, books_patch, books_give
from container import books_service
from dao.models.models_dao import BookSchema
from helpers.decorators import admin_required, auth_required

book_ns = Namespace('books', "Страница для работы с книгами")
book_schema = BookSchema()


@book_ns.route('/')
class BooksViews(Resource):
    @book_ns.expect(books_get)
    @book_ns.response(401, 'Unauthorized')
    @book_ns.marshal_with(book, as_list=True, code=200, description='OK')
    @auth_required
    def get(self):
        """
        Страница для получения информации о всех книгах, доступна всем
        """
        books = books_service.filter_books(**books_get.parse_args())
        return books

    @book_ns.expect(books_post)
    @book_ns.response(201, 'Created')
    @book_ns.response(400, 'BadRequest')
    @book_ns.response(401, 'Unauthorized')
    @book_ns.response(404, 'NotFound')
    @admin_required
    def post(self):
        """
        Страница для добавления новой книги, доступна администратору
        """
        data = request.json
        if not data:
            abort(400)
        books_service.create(data)
        return '', 201


@book_ns.route('/<int:id_>')
class BookViews(Resource):

    @book_ns.response(401, 'Unauthorized')
    @book_ns.response(404, 'NotFound')
    @book_ns.marshal_with(book, code=200, description='OK')
    @auth_required
    def get(self, id_):
        """
        Страница для получения информации о книге, доступна всем
        """
        return books_service.get_one(id_)

    @book_ns.expect(books_put)
    @book_ns.response(204, 'NoContent')
    @book_ns.response(400, 'BadRequest')
    @book_ns.response(401, 'Unauthorized')
    @book_ns.response(404, 'NotFound')
    @admin_required
    def put(self, id_):
        """
        Страница для обновления информации о книге, доступна администратору
        """
        data = request.json
        if not data:
            abort(400)
        data['id'] = id_
        books_service.update(data)
        return '', 204

    @book_ns.expect(books_patch)
    @book_ns.response(204, 'NoContent')
    @book_ns.response(400, 'BadRequest')
    @book_ns.response(401, 'Unauthorized')
    @book_ns.response(404, 'NotFound')
    @admin_required
    def patch(self, id_):
        """
        Страница для частичного обновления книги, доступна администратору
        """
        data = request.json
        if not data:
            abort(400)
        data['id'] = id_
        books_service.update_partial(data)
        return '', 204

    @book_ns.response(204, 'NoContent')
    @book_ns.response(401, 'Unauthorized')
    @book_ns.response(404, 'NotFound')
    @admin_required
    def delete(self, id_):
        """
        Страница для удаления книги, доступна администратору
        """
        books_service.delete(id_)
        return '', 204


@book_ns.route('/give')
class BookGiveViews(Resource):
    @book_ns.response(204, 'NoContent')
    @book_ns.expect(books_give)
    @book_ns.response(400, 'BadRequest')
    @book_ns.response(401, 'Unauthorized')
    @book_ns.response(404, 'NotFound')
    @admin_required
    def post(self):
        """
        Страница для передачи книги читателю, доступна администратору
        """
        data = request.json
        if not data:
            abort(400)
        if ['reader_id', 'book_id'] == data.keys():
            abort(400)
        books_service.give_book_to_reader(data)
        return '', 204


@book_ns.route('/get')
class BookGetViews(Resource):
    @book_ns.expect(books_get)
    @book_ns.response(204, 'NoContent')
    @book_ns.response(400, 'BadRequest')
    @book_ns.response(401, 'Unauthorized')
    @book_ns.response(404, 'NotFound')
    @admin_required
    def post(self):
        """
        Страница для получения книги от читателя, доступна администратору
        :return:
        """
        data = request.json
        if not data:
            abort(400)
        if 'book_id' == data.keys():
            abort(400)
        books_service.get_book_from_reader(data)
        return '', 204
