class TestReaderExceptions:
    url = '/readers/'
    url_all = url + 'all/'

    def test_get_reader_exceptions(self, client, headers_user):
        # Неавторизованный пользователь
        response = client.get(self.url)
        assert response.status_code == 401, f'Возвращается код {response.status_code} вместо 401'

    def test_put_exceptions(self, client, headers_user):
        # Неавторизованный пользователь
        response_1 = client.put(self.url)
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение без данных
        response_2 = client.put(self.url, headers=headers_user)
        assert response_2.status_code == 400, f'Возвращается код {response_2.status_code} вместо 400'

        # Неверные ключи
        data_3 = {
            'wrong_key': "data"
        }
        response_3 = client.put(self.url, json=data_3, headers=headers_user)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

    def test_patch_exceptions(self, client, headers_user):
        # Неавторизованный пользователь
        response_1 = client.patch(self.url)
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение без данных
        response_2 = client.patch(self.url, headers=headers_user)
        assert response_2.status_code == 400, f'Возвращается код {response_2.status_code} вместо 400'

        # Неверные ключи
        data_3 = {
            'wrong_key': "data"
        }
        response_3 = client.patch(self.url, json=data_3, headers=headers_user)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

    def test_get_reader_by_admin_exceptions(self, client, headers_user, reader_2):
        # Неавторизованный пользователь
        response_1 = client.get(f'{self.url}{reader_2.id}/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.get(f'{self.url}{reader_2.id}/', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

    def test_put_reader_by_admin_exceptions(self, client, headers_user, headers_admin, reader_2):
        # Неавторизованный пользователь
        response_1 = client.put(f'{self.url}{reader_2.id}/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.put(f'{self.url}{reader_2.id}/', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Обращение без данных
        response_3 = client.put(f'{self.url}{reader_2.id}/', headers=headers_admin)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            'wrong_key': "data"
        }
        response_4 = client.put(f'{self.url}{reader_2.id}/', json=data_4, headers=headers_admin)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

    def test_patch_reader_by_admin_exceptions(self, client, headers_user, headers_admin, reader_2):
        # Неавторизованный пользователь
        response_1 = client.patch(f'{self.url}{reader_2.id}/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.patch(f'{self.url}{reader_2.id}/', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Обращение без данных
        response_3 = client.patch(f'{self.url}{reader_2.id}/', headers=headers_admin)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            'wrong_key': "data"
        }
        response_4 = client.patch(f'{self.url}{reader_2.id}/', json=data_4, headers=headers_admin)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

    def test_get_all_by_admin(self, client, headers_user):
        # Неавторизованный пользователь
        response_1 = client.get(self.url_all)
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.get(self.url_all, headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'
