class TestGetGiveBookViewsExceptions:
    def test_give_exceptions(self, client, book_1, book_2, reader_1, headers_user, headers_admin):
        # Неавторизованный пользователь
        response_1 = client.post(f'/books/give/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.post(f'/books/give/', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Обращение без данных
        response_3 = client.post(f'/books/give/', headers=headers_admin)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            'key_1': 1,
            'key_2': 2
        }
        response_4 = client.post(f'/books/give/', json=data_4, headers=headers_admin)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Неверные значения
        data_5 = {
            'book_id': None,
            'reader_id': None
        }
        response_5 = client.post(f'/books/give/', json=data_5, headers=headers_admin)
        assert response_5.status_code == 400, f'Возвращается код {response_5.status_code} вместо 400'

        data_6 = {
            'book_id': '1',
            'reader_id': '2'
        }
        response_6 = client.post(f'/books/give/', json=data_6, headers=headers_admin)
        assert response_6.status_code == 400, f'Возвращается код {response_6.status_code} вместо 400'

        # Несуществующая книга
        data_7 = {
            'book_id': 99999,
            'reader_id': reader_1.id
        }
        response_7 = client.post(f'/books/give/', json=data_7, headers=headers_admin)
        assert response_7.status_code == 404, f'Возвращается код {response_7.status_code} вместо 404'

        # Несуществующий читатель
        data_8 = {
            'book_id': book_1.id,
            'reader_id': 99999
        }
        response_8 = client.post(f'/books/give/', json=data_8, headers=headers_admin)
        assert response_8.status_code == 404, f'Возвращается код {response_8.status_code} вместо 404'

        # Книга не в библиотеке
        data_9 = {
            'book_id': book_2.id,
            'reader_id': reader_1.id
        }
        response_9 = client.post(f'/books/give/', json=data_9, headers=headers_admin)
        assert response_9.status_code == 400, f'Возвращается код {response_9.status_code} вместо 400'

    def test_get_exceptions(self, client, book_1, book_2, reader_1, headers_user, headers_admin):
        # Неавторизованный пользователь
        response_1 = client.post(f'/books/get/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.post(f'/books/get/', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Обращение без данных
        response_3 = client.post(f'/books/get/', headers=headers_admin)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            'key_1': 1,
        }
        response_4 = client.post(f'/books/get/', json=data_4, headers=headers_admin)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Неверные значения
        data_5 = {
            'book_id': None,
        }
        response_5 = client.post(f'/books/get/', json=data_5, headers=headers_admin)
        assert response_5.status_code == 400, f'Возвращается код {response_5.status_code} вместо 400'

        data_6 = {
            'book_id': '1',
        }
        response_6 = client.post(f'/books/get/', json=data_6, headers=headers_admin)
        assert response_6.status_code == 400, f'Возвращается код {response_6.status_code} вместо 400'

        # Несуществующая книга
        data_7 = {
            'book_id': 99999,
        }
        response_7 = client.post(f'/books/get/', json=data_7, headers=headers_admin)
        assert response_7.status_code == 404, f'Возвращается код {response_7.status_code} вместо 404'

        # Книга в библиотеке
        data_9 = {
            'book_id': book_1.id,
        }
        response_9 = client.post(f'/books/get/', json=data_9, headers=headers_admin)
        assert response_9.status_code == 400, f'Возвращается код {response_9.status_code} вместо 400'
