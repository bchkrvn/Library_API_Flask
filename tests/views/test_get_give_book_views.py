class TestGetGiveBookViews:
    def test_give(self, client, book_1, reader_1, headers_admin, book_service):
        data = {
            "book_id": book_1.id,
            "reader_id": reader_1.id
        }

        response = client.post('/books/give/', json=data, headers=headers_admin)
        assert response.status_code == 204, f'Возвращается код {response.status_code} вместо 204'

        book = book_service.get_one(book_1.id)

        assert book.is_in_lib is False, 'Книга осталась в библиотеке'
        assert book.reader_id is not None, 'Читатель не установлен'
        assert book.reader_id == data.get("reader_id"), 'Установлен неверный читатель'

    def test_get(self, client, book_2, reader_2, headers_admin, book_service):
        data = {
            "book_id": book_2.id,
        }
        response = client.post('/books/get/', json=data, headers=headers_admin)
        assert response.status_code == 204, f'Возвращается код {response.status_code} вместо 204'

        book = book_service.get_one(book_2.id)

        assert book.is_in_lib is True, 'Книга осталась в библиотеке'
        assert book.reader_id is None, 'Читатель остался'
