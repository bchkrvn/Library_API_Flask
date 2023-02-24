from dao.books_dao import BookDAO
from flask import abort

from dao.models.models_dao import Book


class BookService:
    def __init__(self, dao: BookDAO, author_service, reader_service):
        self.dao = dao
        self.author_service = author_service
        self.reader_service = reader_service

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, id_):
        book = self.dao.get_one(id_)
        if not book:
            abort(404,  f'book with id={id_} not found')
        return book

    def filter_books(self, author_id, reader_id, section):
        result = self.dao.get_all_to_filter()
        if section == 'in':
            result = self.dao.get_by_available(result, True)
        elif section == 'out':
            result = self.dao.get_by_available(result, False)
        elif section in ['all', None]:
            pass
        else:
            abort(400)

        if author_id:
            result = self.dao.get_by_author(result, author_id)
        if reader_id:
            result = self.dao.get_by_reader(result, reader_id)

        return self.dao.get_all(result)

    def create(self, data):
        author_id = data.get('author_id')
        author = self.author_service.get_one(author_id)
        data['is_in_lib'] = True
        new_book = Book(**data)
        self.dao.save(new_book)

    def update(self, data):
        book = self.get_one(data.get('id'))
        book.title = data.get('title')
        book.is_in_lib = data.get('is_in_lib')
        book.author_id = data.get('author_id')
        book.reader_id = data.get('reader_id')
        self.dao.save(book)

    def update_partial(self, data):
        book = self.get_one(data.get('id'))
        if 'title' in data:
            book.title = data.get('title')
        if 'is_in_lib' in data:
            book.is_in_lib = data.get('is_in_lib')
        if 'author_id' in data:
            book.author_id = data.get('author_id')
        if 'reader_id' in data:
            book.reader_id = data.get('reader_id')
        self.dao.save(book)

    def delete(self, id_):
        book = self.get_one(id_)
        self.dao.delete(book)

    def give_book_to_reader(self, data):
        reader_id = data.get('reader_id')
        book_id = data.get('book_id')
        reader = self.reader_service.get_one(reader_id)
        book = self.get_one(book_id)

        if book.is_in_lib:
            book.is_in_lib = False
            book.reader = reader
            self.dao.save(book)
        else:
            abort(400, f'book id={book_id} not in library')

    def get_book_from_reader(self, data):
        book_id = data.get('book_id')
        book = self.get_one(book_id)

        if not book.is_in_lib:
            book.is_in_lib = True
            book.reader_id = None
            self.dao.save(book)
        else:
            abort(400, f'book id={book_id} already in library')
