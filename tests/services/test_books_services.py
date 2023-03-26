import pytest
from werkzeug.exceptions import BadRequest, NotFound

from dao.models.models_dao import Book


class TestBookService:
    def test_get_all(self, book_1, book_2, book_service):
        books = book_service.get_all()

        assert books is not None, "Возвращается None вместо книг"
        assert type(books) is list, 'Возвращается не список'
        assert len(books) == 2, f'Возвращается больше книг({len(books)}), чем ожидалось(2)'
        assert book_1 in books, "Первой книги нет в списке"
        assert book_2 in books, "Второй книги нет в списке"

    def test_get_one(self, book_1, book_service):
        book = book_service.get_one(book_1.id)

        assert book is not None, "Возвращается None вместо книги"
        assert type(book) is Book, f'Возвращается не книга, а {type(book)}'
        assert book.id == book_1.id, "id книги не совпадает"
        assert book.title == book_1.title, "title книг не совпадают"
        assert book.is_in_lib == book_1.is_in_lib, "is_in_lib книг не совпадают"
        assert book.reader_id == book_1.reader_id, "reader_id книг не совпадают"
        assert book.author_id == book_1.author_id, "author_id книг не совпадают"

        with pytest.raises(NotFound):
            book_2 = book_service.get_one(2)

    def test_filter_books(self, book_1, book_2, book_service):
        author_id = book_2.author_id
        reader_id = book_2.reader_id

        author_books = book_service.filter_books(author_id=author_id)
        assert len(author_books) == 1, 'Возвращается больше книг, чем нужно'
        assert book_2 in author_books, 'Нужной книги нету в списке'

        reader_books = book_service.filter_books(reader_id=reader_id)
        assert len(reader_books) == 1, 'Возвращается больше книг, чем нужно'
        assert book_2 in reader_books, 'Нужной книги нету в списке'

        all_books = book_service.filter_books(section='all')
        assert len(all_books) == 2, 'Возвращается меньше книг, чем нужно'
        assert book_1 in all_books, 'Нужной книги нету в списке'
        assert book_2 in all_books, 'Нужной книги нету в списке'

        in_books = book_service.filter_books(section='in')
        assert len(in_books) == 1, 'Возвращается больше книг, чем нужно'
        assert book_1 in in_books, 'Нужной книги нету в списке'

        out_books = book_service.filter_books(section='out')
        assert len(out_books) == 1, 'Возвращается больше книг, чем нужно'
        assert book_2 in out_books, 'Нужной книги нету в списке'

        books = book_service.filter_books(author_id=author_id, reader_id=reader_id, section='out')
        assert len(books) == 1, 'Возвращается больше книг, чем нужно'
        assert book_2 in books, 'Нужной книги нету в списке'

        with pytest.raises(BadRequest):
            book_service.filter_books(section='wrong_section')

    def test_create(self, author_1, book_service):
        data_1 = {
            'title': 'Название',
            'author_id': 1,
        }
        book_service.create(data_1)
        book = book_service.get_all()[-1]

        assert book is not None, "Возвращается None вместо книги"
        assert type(book) is Book, f'Возвращается не книга, а {type(book)}'
        assert book.title == data_1.get('title'), "title книг не совпадают"
        assert book.author == author_1, "author книг не совпадают"

        data_2 = {
            'title': 'Название',
            'author_first_name': author_1.first_name,
            'author_last_name': author_1.last_name
        }
        book_service.create(data_2)
        book = book_service.get_all()[-1]

        assert book is not None, "Возвращается None вместо книги"
        assert type(book) is Book, f'Возвращается не книга, а {type(book)}'
        assert book.title == data_2.get('title'), "title книг не совпадают"
        assert book.author == author_1, "author книг не совпадают"

        # Несуществующий автор
        data_3 = {
            'title': 'Название',
            'author_id': 2,
        }

        with pytest.raises(NotFound):
            book_service.create(data_3)

        data_4 = {
            'title': 'Название',
            'author_first_name': 'Wrong_name',
            'author_last_name': "Wrong_last_name"
        }

        with pytest.raises(NotFound):
            book_service.create(data_4)

    def test_update(self, book_1, reader_1, author_1, book_service):
        data = {
            'id': 1,
            'title': 'Название_1',
            'author_id': 1,
            'reader_id': 1,
            'is_in_lib': False,
        }
        book_service.update(data)
        book = book_service.get_one(book_1.id)

        assert book is not None, "Возвращается None вместо книги"
        assert type(book) is Book, f'Возвращается не книга, а {type(book)}'
        assert book.id == data.get('id'), "id книги не совпадает"
        assert book.title == data.get('title'), "title книг не совпадают"
        assert book.is_in_lib == data.get('is_in_lib'), "is_in_lib книг не совпадают"
        assert book.reader_id == data.get('reader_id'), "reader_id книг не совпадают"
        assert book.author_id == data.get('author_id'), "author_id книг не совпадают"

        data = {
            'id': 1,
            'title': 'Название_1',
            'author_id': 1,
            'reader_id': 1,
            'is_in_lib': True,
        }
        book_service.update(data)
        book = book_service.get_one(book_1.id)

        assert book is not None, "Возвращается None вместо книги"
        assert type(book) is Book, f'Возвращается не книга, а {type(book)}'
        assert book.id == data.get('id'), "id книги не совпадает"
        assert book.title == data.get('title'), "title книг не совпадают"
        assert book.is_in_lib == data.get('is_in_lib'), "is_in_lib книг не совпадают"
        assert book.reader_id is None, "reader_id книг не None"
        assert book.author_id == data.get('author_id'), "author_id книг не совпадают"

    def test_update_wrong(self, book_1, reader_1, author_1, book_service):
        # Несуществующая книга
        data_1 = {
            'id': 2,
            'title': 'Название_1',
            'author_id': 1,
            'reader_id': 1,
            'is_in_lib': True,
        }

        with pytest.raises(NotFound):
            book_service.update(data_1)

        # Несуществующий автор
        data_2 = {
            'id': book_1.id,
            'title': 'Название_1',
            'author_id': 2,
            'reader_id': 1,
            'is_in_lib': True,
        }

        with pytest.raises(NotFound):
            book_service.update(data_2)

        # Несуществующий читатель
        data_3 = {
            'id': book_1.id,
            'title': 'Название_1',
            'author_id': 1,
            'reader_id': 2,
            'is_in_lib': False,
        }

        with pytest.raises(NotFound):
            book_service.update(data_3)

        # is_in_lib не bool
        data_2 = {
            'id': book_1.id,
            'title': 'Название_1',
            'author_id': 2,
            'reader_id': 1,
            'is_in_lib': 'str',
        }

        with pytest.raises(BadRequest):
            book_service.update(data_2)

    def test_update_partial(self, book_1, reader_1, author_1, book_service):
        data = {
            'id': book_1.id,
            'title': 'Название_1',
            'author_id': 1,
            'reader_id': 1,
            'is_in_lib': False,
        }
        book_service.update_partial(data)
        book = book_service.get_one(book_1.id)

        assert book is not None, "Возвращается None вместо книги"
        assert type(book) is Book, f'Возвращается не книга, а {type(book)}'
        assert book.id == data.get('id'), "id книги не совпадает"
        assert book.title == data.get('title'), "title книг не совпадают"
        assert book.is_in_lib == data.get('is_in_lib'), "is_in_lib книг не совпадают"
        assert book.reader_id == data.get('reader_id'), "reader_id книг не совпадают"
        assert book.author_id == data.get('author_id'), "author_id книг не совпадают"

        data = {
            'id': book_1.id,
            'title': 'Название_1',
            'author_id': 1,
            'reader_id': 1,
            'is_in_lib': True,
        }
        book_service.update_partial(data)
        book = book_service.get_one(book_1.id)

        assert book is not None, "Возвращается None вместо книги"
        assert type(book) is Book, f'Возвращается не книга, а {type(book)}'
        assert book.id == data.get('id'), "id книги не совпадает"
        assert book.title == data.get('title'), "title книг не совпадают"
        assert book.is_in_lib == data.get('is_in_lib'), "is_in_lib книг не совпадают"
        assert book.reader_id is None, "reader_id книг не None"
        assert book.author_id == data.get('author_id'), "author_id книг не совпадают"

    def test_update_partial_wrong(self, book_1, reader_1, author_1, book_service):
        # Несуществующая книга
        data_1 = {
            'id': 2,
        }

        with pytest.raises(NotFound):
            book_service.update_partial(data_1)

        # Несуществующий автор
        data_2 = {
            'id': book_1.id,
            'author_id': 2,
        }

        with pytest.raises(NotFound):
            book_service.update_partial(data_2)

        # Несуществующий читатель
        data_3 = {
            'id': book_1.id,
            'is_in_lib': False,
            'reader_id': 2,
        }

        with pytest.raises(NotFound):
            book_service.update_partial(data_3)

        # is_in_lib не bool
        data_4 = {
            'id': book_1.id,
            'is_in_lib': 'str',
        }

        with pytest.raises(BadRequest):
            book_service.update_partial(data_4)

    def test_delete(self, book_1, book_service):
        book_service.delete(book_1.id)
        books = book_service.get_all()

        assert len(books) == 0, 'Книга не удалилась'

        # Неверный id
        with pytest.raises(NotFound):
            book_service.delete(1)

    def test_give_book_to_reader(self, book_1, reader_1, book_service):
        data = {
            'book_id': book_1.id,
            'reader_id': reader_1.id,
        }
        book_service.give_book_to_reader(data)
        book = book_service.get_one(book_1.id)

        assert not book.is_in_lib, 'is_in_lib не равняется False'
        assert book.reader_id == reader_1.id, f"Неправильный читатель у книги({book.reader_id} вместо {reader_1.id})"

    def test_give_book_to_reader_errors(self, book_2, reader_1, book_service):
        # Несуществующая книга
        with pytest.raises(NotFound):
            data = {
                'book_id': 2,
                'reader_id': reader_1.id,
            }
            book_service.give_book_to_reader(data)

        # Несуществующий читатель
        with pytest.raises(NotFound):
            data = {
                'book_id': book_2.id,
                'reader_id': 2,
            }
            book_service.give_book_to_reader(data)

        # Книга не в библиотеке
        with pytest.raises(BadRequest):
            data = {
                'book_id': book_2.id,
                'reader_id': reader_1.id,
            }
            book_service.give_book_to_reader(data)

    def test_get_book_from_reader(self, book_2, book_service):
        data = {
            'book_id': book_2.id,
        }
        book_service.get_book_from_reader(data)
        book = book_service.get_one(book_2.id)

        assert book.is_in_lib, 'is_in_lib не равняется True'
        assert book.reader_id is None, f"У книги остался читатель"

    def test_get_book_from_reader_errors(self, book_1, book_service):
        # Несуществующая книга
        with pytest.raises(NotFound):
            data_1 = {
                'book_id': 2,
            }
            book_service.get_book_from_reader(data_1)

        # Книга уже в библиотеке
        with pytest.raises(BadRequest):
            data_2 = {
                'book_id': book_1.id,
            }
            book_service.get_book_from_reader(data_2)
