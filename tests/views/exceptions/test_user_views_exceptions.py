class TestUserViewsExceptions:
    def test_get_by_user_exceptions(self, client, user_1):
        # Неавторизованный пользователь
        response_1 = client.get('/users/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

    def test_put_by_user_exceptions(self, client, user_1, headers_user):
        # Неавторизованный пользователь
        response_1 = client.put(f'/users/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение без данных
        response_2 = client.put('/users/', headers=headers_user)
        assert response_2.status_code == 400, f'Возвращается код {response_2.status_code} вместо 400'

        # Неверные ключи
        data_3 = {
            'wrong_key': "data"
        }
        response_3 = client.put('/users/', json=data_3, headers=headers_user)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

    def test_get_reader_by_admin_exceptions(self, client, headers_user, user_2):
        # Неавторизованный пользователь
        response_1 = client.get(f'/users/{user_2.id}')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.get(f'/users/{user_2.id}', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

    def test_put_reader_by_admin_exceptions(self, client, headers_user, headers_admin, user_1):
        # Неавторизованный пользователь
        response_1 = client.put(f'/users/{user_1.id}')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.put(f'/users/{user_1.id}', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Обращение без данных
        response_3 = client.put(f'/users/{user_1.id}', headers=headers_admin)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            'wrong_key': "data"
        }
        response_4 = client.put(f'/users/{user_1.id}', json=data_4, headers=headers_admin)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

    def test_get_all_by_admin_exceptions(self, client, headers_user):
        # Неавторизованный пользователь
        response_1 = client.get(f'/users/all')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.get(f'/users/all', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

    def test_register_exceptions(self, client, user_1):
        # Обращение без данных
        response_1 = client.post(f'/users/register')
        assert response_1.status_code == 400, f'Возвращается код {response_1.status_code} вместо 400'

        # Неверные ключи
        data_2 = {
            'wrong_key': "data"
        }
        response_2 = client.post(f'/users/register', json=data_2)
        assert response_2.status_code == 400, f'Возвращается код {response_2.status_code} вместо 400'

        # Пустые значения
        data_3 = {
            "username": None,
            "password": None
        }
        response_3 = client.post(f'/users/register', json=data_3)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        data_4 = {
            "username": "",
            "password": ""
        }
        response_4 = client.post(f'/users/register', json=data_4)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Существующий username
        data_5 = {
            "username": user_1.username,
            "password": "1234"
        }
        response_5 = client.post(f'/users/register', json=data_5)
        assert response_5.status_code == 400, f'Возвращается код {response_5.status_code} вместо 400'

    def test_change_password_exceptions(self, client, user_1, headers_user):
        # Неавторизованный пользователь
        response_1 = client.post(f'/users/password')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение без данных
        response_2 = client.post(f'/users/password', headers=headers_user)
        assert response_2.status_code == 400, f'Возвращается код {response_2.status_code} вместо 400'

        # Неверные ключи
        data_3 = {
            'wrong_key': "data"
        }
        response_3 = client.post(f'/users/password', json=data_3, headers=headers_user)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Пустые значения
        data_4 = {
            "old_password": None,
            "new_password": None
        }
        response_4 = client.post(f'/users/password', json=data_4, headers=headers_user)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        data_5 = {
            "old_password": "",
            "new_password": ""
        }
        response_5 = client.post(f'/users/password', json=data_5, headers=headers_user)
        assert response_5.status_code == 400, f'Возвращается код {response_5.status_code} вместо 400'

        # Неправильный старый пароль
        data_6 = {
            "old_password": "wrong_password",
            "new_password": ""
        }
        response_6 = client.post(f'/users/password', json=data_6, headers=headers_user)
        assert response_6.status_code == 400, f'Возвращается код {response_6.status_code} вместо 400'
