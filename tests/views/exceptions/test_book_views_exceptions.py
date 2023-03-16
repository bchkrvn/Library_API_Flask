class TestBookViewsExceptions:
    def test_get_books_exceptions(self, client):
        # Неавторизованный пользователь
        response = client.get('/books/')
        assert response.status_code == 401, f'Возвращается код {response.status_code} вместо 401'

    def test_post_exception(self, client, headers_user, author_1, headers_admin):
        # Неавторизованный пользователь
        response_1 = client.post('/books/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.post('/books/', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Обращение без данных
        response_3 = client.post('/books/', headers=headers_admin)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            "key_1": "Название_новое",
            "key_2": 2
        }
        response_4 = client.post('/books/', json=data_4, headers=headers_admin)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Несуществующий автор
        data_5 = {
            "title": "Название",
            "author_id": 2
        }
        response_5 = client.post('/books/', json=data_5, headers=headers_admin)
        assert response_5.status_code == 404, f'Возвращается код {response_5.status_code} вместо 404'

        # Пустые значения
        data_6 = {
            "key_1": "",
            "key_2": None
        }
        response_6 = client.post('/books/', json=data_6, headers=headers_admin)
        assert response_6.status_code == 400, f'Возвращается код {response_6.status_code} вместо 400'

    def test_get_book_exceptions(self, client, book_1, headers_user):
        # Неавторизованный пользователь
        response_1 = client.get(f'/books/{book_1.id}')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Несуществующая книга
        response_2 = client.get(f'/books/9999', headers=headers_user)
        assert response_2.status_code == 404, f'Возвращается код {response_2.status_code} вместо 404'

    def test_put_exceptions(self, client, book_1, author_1, reader_1, headers_user, headers_admin):
        # Неавторизованный пользователь
        response_1 = client.put(f'/books/{book_1.id}')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.put(f'/books/{book_1.id}', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Обращение без данных
        response_3 = client.put(f'/books/{book_1.id}', headers=headers_admin)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            "key_1": "Название",
            "key_2": 2
        }
        response_4 = client.put(f'/books/{book_1.id}', json=data_4, headers=headers_admin)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Несуществующий автор
        data_5 = {
            "title": "Новое название",
            "author_id": 99999,
            "reader_id": reader_1.id,
            "is_in_lib": False
        }
        response_5 = client.put(f'/books/{book_1.id}', json=data_5, headers=headers_admin)
        assert response_5.status_code == 404, f'Возвращается код {response_5.status_code} вместо 404'

        # Несуществующий читатель
        data_5 = {
            "title": "Новое название",
            "author_id": author_1.id,
            "reader_id": 999999,
            "is_in_lib": False
        }
        response_5 = client.put(f'/books/{book_1.id}', json=data_5, headers=headers_admin)
        assert response_5.status_code == 404, f'Возвращается код {response_5.status_code} вместо 404'

        # Пустые значения
        data_6 = {
            "title": "",
            "author_id": None,
            "reader_id": None,
            "is_in_lib": None
        }
        response_6 = client.put(f'/books/{book_1.id}', json=data_6, headers=headers_admin)
        assert response_6.status_code == 400, f'Возвращается код {response_6.status_code} вместо 400'

        # Не в библиотеке без читателя
        data_6 = {
            "title": "Название",
            "author_id": author_1.id,
            "reader_id": None,
            "is_in_lib": False
        }
        response_6 = client.put(f'/books/{book_1.id}', json=data_6, headers=headers_admin)
        assert response_6.status_code == 400, f'Возвращается код {response_6.status_code} вместо 400'

    def test_patch_exceptions(self, client, book_1, author_1, reader_1, headers_user, headers_admin):
        # Неавторизованный пользователь
        response_1 = client.patch(f'/books/{book_1.id}')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.patch(f'/books/{book_1.id}', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Обращение без данных
        response_3 = client.patch(f'/books/{book_1.id}', headers=headers_admin)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            "key_1": "Название",
            "key_2": 2
        }
        response_4 = client.patch(f'/books/{book_1.id}', json=data_4, headers=headers_admin)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Несуществующий автор
        data_5 = {
            "title": "Новое название",
            "author_id": 99999,
        }
        response_5 = client.patch(f'/books/{book_1.id}', json=data_5, headers=headers_admin)
        assert response_5.status_code == 404, f'Возвращается код {response_5.status_code} вместо 404'

        # Несуществующий читатель
        data_5 = {
            "reader_id": 999999,
            "is_in_lib": False
        }
        response_5 = client.patch(f'/books/{book_1.id}', json=data_5, headers=headers_admin)
        assert response_5.status_code == 404, f'Возвращается код {response_5.status_code} вместо 404'

        # Пустые значения
        data_6 = {
            "title": "",
            "author_id": None,
            "reader_id": None,
            "is_in_lib": None
        }
        response_6 = client.patch(f'/books/{book_1.id}', json=data_6, headers=headers_admin)
        assert response_6.status_code == 400, f'Возвращается код {response_6.status_code} вместо 400'

        # Не в библиотеке без читателя
        data_6 = {
            "reader_id": None,
            "is_in_lib": False
        }
        response_6 = client.patch(f'/books/{book_1.id}', json=data_6, headers=headers_admin)
        assert response_6.status_code == 400, f'Возвращается код {response_6.status_code} вместо 400'

    def test_delete_exceptions(self, client, headers_user, headers_admin, book_1):
        # Неавторизованный пользователь
        response_1 = client.delete(f'/books/{book_1.id}')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.delete(f'/books/{book_1.id}', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Несуществующая книга
        response_2 = client.delete(f'/books/9999', headers=headers_admin)
        assert response_2.status_code == 404, f'Возвращается код {response_2.status_code} вместо 404'
