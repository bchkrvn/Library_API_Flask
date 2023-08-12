class TestBookViewsExceptions:
    url = '/books/'
    def test_get_books_exceptions(self, client):
        # Неавторизованный пользователь
        response = client.get(self.url)
        assert response.status_code == 401, f'Возвращается код {response.status_code} вместо 401'

    def test_post_exception(self, client, headers_user, author_1, headers_admin):
        # Неавторизованный пользователь
        response_1 = client.post(self.url)
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.post(self.url, headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Обращение без данных
        response_3 = client.post(self.url, headers=headers_admin)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            "key_1": "Название_новое",
            "key_2": 2
        }
        response_4 = client.post(self.url, json=data_4, headers=headers_admin)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Несуществующий автор
        data_5 = {
            "title": "Название",
            "author_id": 2
        }
        response_5 = client.post(self.url, json=data_5, headers=headers_admin)
        assert response_5.status_code == 404, f'Возвращается код {response_5.status_code} вместо 404'

        data_6 = {
            "title": "Название",
            "author_first_name": 'Wrong_first_name',
            "author_last_name": 'Wrong_last_name'
        }
        response_6 = client.post(self.url, json=data_6, headers=headers_admin)
        assert response_6.status_code == 404, f'Возвращается код {response_6.status_code} вместо 404'

        # Пустые значения
        data_7 = {
            "title": "",
            "author_id": ""
        }
        response_7 = client.post(self.url, json=data_7, headers=headers_admin)
        assert response_7.status_code == 400, f'Возвращается код {response_7.status_code} вместо 400'

        data_8 = {
            "title": None,
            "author_id": None
        }
        response_8 = client.post(self.url, json=data_8, headers=headers_admin)
        assert response_8.status_code == 400, f'Возвращается код {response_8.status_code} вместо 400'

    def test_get_book_exceptions(self, client, book_1, headers_user):
        # Неавторизованный пользователь
        response_1 = client.get(f'{self.url}{book_1.id}/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Несуществующая книга
        response_2 = client.get(f'{self.url}9999/', headers=headers_user)
        assert response_2.status_code == 404, f'Возвращается код {response_2.status_code} вместо 404'

    def test_put_exceptions(self, client, book_1, author_1, reader_1, headers_user, headers_admin):
        # Неавторизованный пользователь
        response_1 = client.put(f'{self.url}{book_1.id}/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.put(f'{self.url}{book_1.id}/', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Обращение без данных
        response_3 = client.put(f'{self.url}{book_1.id}/', headers=headers_admin)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            "key_1": "Название",
            "key_2": 2
        }
        response_4 = client.put(f'{self.url}{book_1.id}/', json=data_4, headers=headers_admin)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Несуществующий автор
        data_5 = {
            "title": "Новое название",
            "author_id": 99999,
            "reader_id": reader_1.id,
            "is_in_lib": False
        }
        response_5 = client.put(f'{self.url}{book_1.id}/', json=data_5, headers=headers_admin)
        assert response_5.status_code == 404, f'Возвращается код {response_5.status_code} вместо 404'

        data_6 = {
            "title": "Новое название",
            "author_first_name": 'Wrong_first_name',
            "author_last_name": 'Wrong_last_name',
            "reader_id": reader_1.id,
            "is_in_lib": False
        }
        response_6 = client.put(f'{self.url}{book_1.id}/', json=data_6, headers=headers_admin)
        assert response_6.status_code == 404, f'Возвращается код {response_6.status_code} вместо 404'

        data_6 = {
            "title": "Новое название",
            "author_first_name": author_1.first_name,
            "reader_id": reader_1.id,
            "is_in_lib": False
        }
        response_6 = client.put(f'{self.url}{book_1.id}/', json=data_6, headers=headers_admin)
        assert response_6.status_code == 400, f'Возвращается код {response_6.status_code} вместо 404'

        # Несуществующий читатель
        data_7 = {
            "title": "Новое название",
            "author_id": author_1.id,
            "reader_id": 999999,
            "is_in_lib": False
        }
        response_7 = client.put(f'{self.url}{book_1.id}/', json=data_7, headers=headers_admin)
        assert response_7.status_code == 404, f'Возвращается код {response_7.status_code} вместо 404'

        # Пустые значения
        data_8 = {
            "title": None,
            "author_id": None,
            "reader_id": None,
            "is_in_lib": None
        }
        response_8 = client.put(f'{self.url}{book_1.id}/', json=data_8, headers=headers_admin)
        assert response_8.status_code == 400, f'Возвращается код {response_8.status_code} вместо 400'

        data_9 = {
            "title": "",
            "author_id": "",
            "reader_id": "",
            "is_in_lib": ""
        }
        response_9 = client.put(f'{self.url}{book_1.id}/', json=data_9, headers=headers_admin)
        assert response_9.status_code == 400, f'Возвращается код {response_9.status_code} вместо 400'

        # Не в библиотеке без читателя
        data_10 = {
            "title": "Название",
            "author_id": author_1.id,
            "reader_id": None,
            "is_in_lib": False
        }
        response_10 = client.put(f'{self.url}{book_1.id}/', json=data_10, headers=headers_admin)
        assert response_10.status_code == 400, f'Возвращается код {response_10.status_code} вместо 400'

    def test_patch_exceptions(self, client, book_1, author_1, reader_1, headers_user, headers_admin):
        # Неавторизованный пользователь
        response_1 = client.patch(f'{self.url}{book_1.id}/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.patch(f'{self.url}{book_1.id}/', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Обращение без данных
        response_3 = client.patch(f'{self.url}{book_1.id}/', headers=headers_admin)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            "key_1": "Название",
            "key_2": 2
        }
        response_4 = client.patch(f'{self.url}{book_1.id}/', json=data_4, headers=headers_admin)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Несуществующий автор
        data_5 = {
            "title": "Новое название",
            "author_id": 99999,
        }
        response_5 = client.patch(f'{self.url}{book_1.id}/', json=data_5, headers=headers_admin)
        assert response_5.status_code == 404, f'Возвращается код {response_5.status_code} вместо 404'

        data_6 = {
            "title": "Новое название",
            "author_first_name": 'Wrong_first_name',
            "author_last_name": 'Wrong_last_name'
        }
        response_6 = client.patch(f'{self.url}{book_1.id}/', json=data_6, headers=headers_admin)
        assert response_6.status_code == 404, f'Возвращается код {response_6.status_code} вместо 404'

        data_6 = {
            "title": "Новое название",
            "author_first_name": author_1.first_name,
        }
        response_6 = client.patch(f'{self.url}{book_1.id}/', json=data_6, headers=headers_admin)
        assert response_6.status_code == 400, f'Возвращается код {response_6.status_code} вместо 404'

        # Несуществующий читатель
        data_7 = {
            "reader_id": 999999,
            "is_in_lib": False
        }
        response_7 = client.patch(f'{self.url}{book_1.id}/', json=data_7, headers=headers_admin)
        assert response_7.status_code == 404, f'Возвращается код {response_7.status_code} вместо 404'

        # Пустые значения
        data_8 = {
            "title": None,
            "author_id": None,
            "reader_id": None,
            "is_in_lib": None
        }
        response_8 = client.patch(f'{self.url}{book_1.id}/', json=data_8, headers=headers_admin)
        assert response_8.status_code == 400, f'Возвращается код {response_8.status_code} вместо 400'

        data_9 = {
            "title": "",
            "author_id": "",
            "reader_id": "",
            "is_in_lib": ""
        }
        response_9 = client.patch(f'{self.url}{book_1.id}/', json=data_9, headers=headers_admin)
        assert response_9.status_code == 400, f'Возвращается код {response_9.status_code} вместо 400'

        # Не в библиотеке без читателя
        data_10 = {
            "reader_id": None,
            "is_in_lib": False
        }
        response_10 = client.patch(f'{self.url}{book_1.id}/', json=data_10, headers=headers_admin)
        assert response_10.status_code == 400, f'Возвращается код {response_10.status_code} вместо 400'

    def test_delete_exceptions(self, client, headers_user, headers_admin, book_1):
        # Неавторизованный пользователь
        response_1 = client.delete(f'{self.url}{book_1.id}/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.delete(f'{self.url}{book_1.id}/', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Несуществующая книга
        response_2 = client.delete(f'{self.url}9999/', headers=headers_admin)
        assert response_2.status_code == 404, f'Возвращается код {response_2.status_code} вместо 404'
