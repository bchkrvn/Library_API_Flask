from dao.books_dao import BookDAO
from flask import abort

from dao.models.models_dao import Book
from services.authors_service import AuthorService
from services.readers_service import ReaderService


class BookService:
    """
    Сервис для работы с книгами
    """

    def __init__(self, dao: BookDAO, author_service: AuthorService, reader_service: ReaderService):
        self.dao = dao
        self.author_service = author_service
        self.reader_service = reader_service

    def get_all(self) -> list[Book]:
        """
        Получить список всех книг
        :return: list[Book]
        """
        return self.dao.get_all()

    def get_one(self, id_: int) -> Book:
        """
        Получить книгу по ее id
        :param id_: id книги
        :return: Book
        """
        book = self.dao.get_one(id_)
        if not book:
            abort(404, f'book with id={id_} not found')
        return book

    def filter_books(self, author_id=None, reader_id=None, section=None) -> list[Book]:
        """
        Получить отфильтрованный список книг.
        Отфильтровать можно по автору, читателю и наличию
        :param author_id: id автора книги
        :param reader_id: id читателя
        :param section: наличие книги (in, out, all)
        :return: list[Book]
        """
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

    def create(self, data: dict):
        """
        Добавить новую книгу
        :param data: данные о книге (название, автор)
        """
        if 'author_id' in data:
            author_id = data.pop('author_id')
            author = self.author_service.get_one(author_id)
        else:
            first_name = data.pop('author_first_name')
            last_name = data.pop('author_last_name')
            author = self.author_service.get_by_name(first_name, last_name)
        data['author'] = author
        data['is_in_lib'] = True
        new_book = Book(**data)
        self.dao.save(new_book)

    def update(self, data: dict):
        """
        Обновить информацию о книге
        :param data: информация для обновления (название, автор)
        """
        book = self.get_one(data.get('id'))
        book.title = data.get('title')
        is_in_lib = data.get('is_in_lib')
        reader_id = data.get('reader_id')

        if type(is_in_lib) is bool:
            book.is_in_lib = data.get('is_in_lib')
        else:
            abort(400, 'Wrong data')

        book.author = self.author_service.get_one(data.get('author_id'))

        if is_in_lib:
            book.reader = None
        elif reader_id:
            book.reader = self.reader_service.get_one(data.get('reader_id'))
        else:
            abort(400, "Didn't send reader_id if not in lib")

        self.dao.save(book)

    def update_partial(self, data: dict):
        """
        Частично обновить информацию о книге
        :param data: информация для обновления (название, автор)
        """
        book = self.get_one(data.get('id'))
        title = data.get('title', None)
        if title:
            book.title = title

        author_id = data.get('author_id', None)
        if author_id:
            book.author = self.author_service.get_one(author_id)

        is_in_lib = data.get('is_in_lib', None)
        reader_id = data.get('reader_id', None)

        if type(is_in_lib) is bool:

            if is_in_lib:
                book.is_in_lib = is_in_lib
                book.reader_id = None
            elif reader_id:
                book.is_in_lib = is_in_lib
                book.reader = self.reader_service.get_one(reader_id)
            else:
                abort(400, "Didn't send reader_id if not in lib")

        elif is_in_lib is not None:
            abort(400, 'is in lib must be bool')

        self.dao.save(book)

    def delete(self, id_: int):
        """
        Удалить книгу по ее id
        :param id_: id книги
        :return:
        """
        book = self.get_one(id_)
        self.dao.delete(book)

    def give_book_to_reader(self, data: dict):
        """
        Передать книгу читателю
        :param data: данные, содержащие id книги и id читателя
        :return:
        """
        reader_id = data.get('reader_id')
        reader = self.reader_service.get_one(reader_id)

        book_id = data.get('book_id')
        book = self.get_one(book_id)

        if book.is_in_lib:
            book.is_in_lib = False
            book.reader = reader
            self.dao.save(book)
        else:
            abort(400, f'Book id={book_id} not in library')

    def get_book_from_reader(self, data: dict):
        """
        Получить книгу от читателя
        :param data: данные, содержащие id книги
        """
        book_id = data.get('book_id')
        book = self.get_one(book_id)

        if not book.is_in_lib:
            book.is_in_lib = True
            book.reader_id = None
            self.dao.save(book)
        else:
            abort(400, f'book id={book_id} already in library')
