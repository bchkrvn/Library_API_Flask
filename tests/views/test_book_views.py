class TestBookViews:
    def test_get_books(self, client, book_1, book_2, author_2, reader_2, headers_user):
        response = client.get('/books/', headers=headers_user)
        assert response.status_code == 200, f'Возвращается код {response.status_code} вместо 200'

        books = response.json
        book_keys = {'id', 'title', 'is_in_lib', 'author', 'reader'}
        assert books is not None, 'Возвращается None или пустой список'
        assert type(books) is list, f'Возвращается {type(books)} вместо list'
        assert type(books[0]) is dict, f'В списке находятся {type(books[0])} вместо dict'
        assert book_keys == set(books[0].keys()), f'Ключи не совпадают'

    def test_post_book(self, client, headers_admin, book_service, author_1):
        data_1 = {
            "title": "Название_1",
            "author_id": author_1.id
        }
        response = client.post('/books/', json=data_1, headers=headers_admin)
        assert response.status_code == 201, f'Возвращается код {response.status_code} вместо 201'

        book = book_service.get_all()[-1]
        assert book is not None, f'Вместо автора вернулся None'
        assert book.title == data_1.get('title'), 'Неверное название книги'
        assert book.author == author_1, 'Неверный автор книги'

        data_2 = {
            'title': 'Название_2',
            'author_first_name': author_1.first_name,
            'author_last_name': author_1.last_name
        }
        response = client.post('/books/', json=data_2, headers=headers_admin)
        assert response.status_code == 201, f'Возвращается код {response.status_code} вместо 201'

        book = book_service.get_all()[-1]
        assert book is not None, f'Вместо автора вернулся None'
        assert book.title == data_2.get('title'), 'Неверное название книги'
        assert book.author == author_1, 'Неверный автор книги'

    def test_get_book(self, client, book_1, headers_user):
        response = client.get(f'/books/{book_1.id}/', headers=headers_user)
        assert response.status_code == 200, f'Возвращается код {response.status_code} вместо 200'

        book = response.json
        book_keys = {'id', 'title', 'is_in_lib', 'author', 'reader'}
        assert book is not None, 'Возвращается None или пустой список'
        assert type(book) is dict, f'В списке находятся {type(book)} вместо dict'
        assert book_keys == set(book.keys()), f'Ключи не совпадают'

    def test_put(self, client, book_1, author_2, author_1, reader_2, headers_admin, book_service):
        data_1 = {
            "title": "Новое название",
            "author_id": author_2.id,
            "reader_id": reader_2.id,
            "is_in_lib": False
        }
        response_1 = client.put(f'/books/{book_1.id}/', json=data_1, headers=headers_admin)
        assert response_1.status_code == 204, f'Возвращается код {response_1.status_code} вместо 204'

        book = book_service.get_one(book_1.id)
        assert book is not None, 'Вместо книги вернулся None'
        assert book.title == data_1.get('title'), 'Название книги не обновилось'
        assert book.author_id == data_1.get('author_id'), 'Автор книги не обновился'
        assert book.reader_id == data_1.get('reader_id'), 'Читатель книги не обновился'
        assert book.is_in_lib == data_1.get('is_in_lib'), 'Наличие книги не обновилось'

        data_2 = {
            "title": "Новое название 2",
            'author_first_name': author_1.first_name,
            'author_last_name': author_1.last_name,
            "reader_id": reader_2.id,
            "is_in_lib": True
        }
        response_2 = client.put(f'/books/{book_1.id}/', json=data_2, headers=headers_admin)
        assert response_2.status_code == 204, f'Возвращается код {response_2.status_code} вместо 204'

        book = book_service.get_one(book_1.id)
        assert book is not None, 'Вместо книги вернулся None'
        assert book.title == data_2.get('title'), 'Название книги не обновилось'
        assert book.author == author_1, 'Автор книги не обновился'
        assert book.reader_id is None, 'Читатель книги не None'
        assert book.is_in_lib == data_2.get('is_in_lib'), 'Наличие книги не обновилось'

    def test_patch(self, client, book_1, author_2, author_1, reader_2, headers_admin, book_service):
        data_1 = {
            "title": "Новое название",
            "author_id": author_2.id,
            "reader_id": reader_2.id,
            "is_in_lib": False
        }
        response_1 = client.patch(f'/books/{book_1.id}/', json=data_1, headers=headers_admin)
        assert response_1.status_code == 204, f'Возвращается код {response_1.status_code} вместо 204'

        book = book_service.get_one(book_1.id)
        assert book is not None, 'Вместо книги вернулся None'
        assert book.title == data_1.get('title'), 'Название книги не обновилось'
        assert book.author == author_2, 'Автор книги не обновился'
        assert book.reader == reader_2, 'Читатель книги не обновился'
        assert book.is_in_lib == data_1.get('is_in_lib'), 'Наличие книги не обновилось'

        data_2 = {
            "title": "Новое название 2",
            'author_first_name': author_1.first_name,
            'author_last_name': author_1.last_name,
            "reader_id": reader_2.id,
            "is_in_lib": True
        }
        response_2 = client.patch(f'/books/{book_1.id}/', json=data_2, headers=headers_admin)
        assert response_2.status_code == 204, f'Возвращается код {response_2.status_code} вместо 204'

        book = book_service.get_one(book_1.id)
        assert book is not None, 'Вместо книги вернулся None'
        assert book.title == data_2.get('title'), 'Название книги не обновилось'
        assert book.author == author_1, 'Автор книги не обновился'
        assert book.reader_id is None, 'Читатель книги не None'
        assert book.is_in_lib == data_2.get('is_in_lib'), 'Наличие книги не обновилось'

    def test_delete(self, client, book_1, book_2, headers_admin, book_service):
        response = client.delete(f'/books/{book_1.id}/', headers=headers_admin)
        assert response.status_code == 204, f'Возвращается код {response.status_code} вместо 204'

        books = book_service.get_all()

        assert len(books) == 1, 'Книга не удалилась'
        assert book_2 in books, 'Удалилась не та книга'
        assert book_1 not in books, 'Нужная книга не удалилась'
