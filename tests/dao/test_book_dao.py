from app.dao.models.models_dao import Book


class TestBookDAO:
    def test_get_all(self, book_1, book_2, book_dao):
        books = book_dao.get_all()

        assert books is not None, "Возвращается None вместо книг"
        assert type(books) is list, 'Возвращается не список'
        assert len(books) == 2, f'Возвращается больше книг({len(books)}), чем ожидалось(2)'
        assert book_1 in books, "Первой книги нет в списке"
        assert book_2 in books, "Второй книги нет в списке"

    def test_get_one(self, book_1, book_dao):
        book = book_dao.get_one(book_1.id)

        assert book is not None, "Возвращается None вместо книги"
        assert type(book) is Book, f'Возвращается не книга, а {type(book)}'
        assert book.id == book_1.id, "id книги не совпадает"
        assert book.title == book_1.title, "title книг не совпадают"
        assert book.is_in_lib == book_1.is_in_lib, "is_in_lib книг не совпадают"
        assert book.reader_id == book_1.reader_id, "reader_id книг не совпадают"
        assert book.author_id == book_1.author_id, "author_id книг не совпадают"

        book_2 = book_dao.get_one(2)

        assert book_2 is None, f'Возвращается {type(book_2)} вместо None'

    def test_get_by_author(self, book_1, book_dao):
        request_1 = book_dao.get_all_to_filter()
        request_2 = book_dao.get_by_author(request_1, book_1.author_id)
        books = book_dao.get_all(request_2)

        assert books is not None, "Возвращается None вместо книг"
        assert type(books) is list, 'Возвращается не список'
        assert len(books) == 1, f'Возвращается больше книг({len(books)}), чем ожидалось(1)'
        assert book_1 in books, "Первой книги нет в списке"

        request_3 = book_dao.get_all_to_filter()
        request_4 = book_dao.get_by_author(request_3, 2)
        books = book_dao.get_all(request_4)

        assert len(books) == 0, 'Возвращается не пустой список'

    def test_get_by_reader(self, book_1, book_dao):
        request_1 = book_dao.get_all_to_filter()
        request_2 = book_dao.get_by_reader(request_1, book_1.reader_id)
        books = book_dao.get_all(request_2)

        assert books is not None, "Возвращается None вместо книг"
        assert type(books) is list, 'Возвращается не список'
        assert len(books) == 1, f'Возвращается больше книг({len(books)}), чем ожидалось(1)'
        assert book_1 in books, "Первой книги нет в списке"

        request_3 = book_dao.get_all_to_filter()
        request_4 = book_dao.get_by_reader(request_3, 2)
        books = book_dao.get_all(request_4)

        assert len(books) == 0, 'Возвращается не пустой список'

    def test_get_by_available(self, book_1, book_dao):
        request_1 = book_dao.get_all_to_filter()
        request_2 = book_dao.get_by_available(request_1, book_1.is_in_lib)
        books = book_dao.get_all(request_2)

        assert books is not None, "Возвращается None вместо книг"
        assert type(books) is list, 'Возвращается не список'
        assert len(books) == 1, f'Возвращается больше книг({len(books)}), чем ожидалось(1)'
        assert book_1 in books, "Первой книги нет в списке"

        request_3 = book_dao.get_all_to_filter()
        request_4 = book_dao.get_by_available(request_3, False)
        books = book_dao.get_all(request_4)

        assert len(books) == 0, 'Возвращается не пустой список'

    def test_save(self, book_dao):
        b = Book(
            title='Название_1',
            is_in_lib=True,
            author_id=1,
            reader_id=1,
        )
        book_dao.save(b)
        book = book_dao.get_all()[-1]

        assert book is not None, "Возвращается None вместо книги"
        assert type(book) is Book, f'Возвращается не книга, а {type(book)}'
        assert book.id == b.id, "id книги не совпадает"
        assert book.title == b.title, "title книг не совпадают"
        assert book.is_in_lib == b.is_in_lib, "is_in_lib книг не совпадают"
        assert book.reader_id == b.reader_id, "reader_id книг не совпадают"
        assert book.author_id == b.author_id, "author_id книг не совпадают"

    def test_delete(self, book_1, book_dao):
        book_dao.delete(book_1)
        books = book_dao.get_all()

        assert len(books) == 0, 'Книга не удалилась'

