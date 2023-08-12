class TestUserViewsExceptions:
    url = '/users/'
    url_all = url + 'all/'
    url_register = url + 'register/'
    url_password = url + 'password/'

    def test_get_by_user_exceptions(self, client, user_1):
        # Неавторизованный пользователь
        response_1 = client.get(self.url)
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

    def test_put_by_user_exceptions(self, client, user_1, user_2, headers_user):
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

        # Username уже занят
        data_4 = {
            'username': user_2.username
        }
        response_4 = client.put(self.url, json=data_4, headers=headers_user)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

    def test_get_user_by_admin_exceptions(self, client, headers_user, user_2):
        # Неавторизованный пользователь
        response_1 = client.get(f'{self.url}{user_2.id}/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.get(f'{self.url}{user_2.id}/', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

    def test_put_user_by_admin_exceptions(self, client, headers_user, headers_admin, user_1, user_2):
        # Неавторизованный пользователь
        response_1 = client.put(f'{self.url}{user_1.id}/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.put(f'{self.url}{user_1.id}/', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Обращение без данных
        response_3 = client.put(f'{self.url}{user_1.id}/', headers=headers_admin)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            'wrong_key': "data"
        }
        response_4 = client.put(f'{self.url}{user_1.id}/', json=data_4, headers=headers_admin)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Username уже занят
        data_5 = {
            'username': user_2.username
        }
        response_5 = client.put(self.url, json=data_5, headers=headers_admin)
        assert response_5.status_code == 400, f'Возвращается код {response_5.status_code} вместо 400'

    def test_get_all_by_admin_exceptions(self, client, headers_user):
        # Неавторизованный пользователь
        response_1 = client.get(self.url_all)
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.get(self.url_all, headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

    def test_register_exceptions(self, client, user_1):
        # Обращение без данных
        response_1 = client.post(self.url_register)
        assert response_1.status_code == 400, f'Возвращается код {response_1.status_code} вместо 400'

        # Неверные ключи
        data_2 = {
            'wrong_key': "data"
        }
        response_2 = client.post(self.url_register, json=data_2)
        assert response_2.status_code == 400, f'Возвращается код {response_2.status_code} вместо 400'

        # Пустые значения
        data_3 = {
            "username": None,
            "password": None
        }
        response_3 = client.post(self.url_register, json=data_3)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        data_4 = {
            "username": "",
            "password": ""
        }
        response_4 = client.post(self.url_register, json=data_4)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Существующий username
        data_5 = {
            "username": user_1.username,
            "password": "1234"
        }
        response_5 = client.post(self.url_register, json=data_5)
        assert response_5.status_code == 400, f'Возвращается код {response_5.status_code} вместо 400'

        # Легкий пароль
        data_6 = {
            "username": 'new_user',
            "password": "1234"
        }
        response_6 = client.post(self.url_register, json=data_6)
        assert response_6.status_code == 400, f'Возвращается код {response_6.status_code} вместо 400'

    def test_change_password_exceptions(self, client, user_1, hard_password_1, headers_user):
        # Неавторизованный пользователь
        response_1 = client.post(self.url_password)
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение без данных
        response_2 = client.post(self.url_password, headers=headers_user)
        assert response_2.status_code == 400, f'Возвращается код {response_2.status_code} вместо 400'

        # Неверные ключи
        data_3 = {
            'wrong_key': "data"
        }
        response_3 = client.post(self.url_password, json=data_3, headers=headers_user)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Пустые значения
        data_4 = {
            "old_password": None,
            "new_password": None
        }
        response_4 = client.post(self.url_password, json=data_4, headers=headers_user)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        data_5 = {
            "old_password": "",
            "new_password": ""
        }
        response_5 = client.post(self.url_password, json=data_5, headers=headers_user)
        assert response_5.status_code == 400, f'Возвращается код {response_5.status_code} вместо 400'

        # Неправильный старый пароль
        data_6 = {
            "old_password": "wrong_password",
            "new_password": ""
        }
        response_6 = client.post(self.url_password, json=data_6, headers=headers_user)
        assert response_6.status_code == 400, f'Возвращается код {response_6.status_code} вместо 400'

        # Легкий пароль
        data_7 = {
            "username": hard_password_1,
            "password": "1234"
        }
        response_7 = client.post(self.url_password, json=data_7, headers=headers_user)
        assert response_7.status_code == 400, f'Возвращается код {response_7.status_code} вместо 400'

    def test_delete_by_user_exceptions(self, client, user_1, user_2, book_2, headers_admin):
        # Неавторизованный пользователь
        response_1 = client.delete(self.url)
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Сданы не все книги
        response_2 = client.delete(f'{self.url}{user_2.id}/', headers=headers_admin)
        assert response_2.status_code == 400, f'Возвращается код {response_2.status_code} вместо 400'
