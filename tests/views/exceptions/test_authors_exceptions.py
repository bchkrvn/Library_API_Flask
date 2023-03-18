class TestAuthorViewsExceptions:
    def test_get_authors_exceptions(self, client):
        # Неавторизованный пользователь
        response = client.get('/authors/')
        assert response.status_code == 401, f'Возвращается код {response.status_code} вместо 401'

    def test_post_exceptions(self, client, headers_admin, headers_user):
        # Неавторизованный пользователь
        response_1 = client.post('/authors/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не администратора
        response_2 = client.post('/authors/', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Обращение без данных
        response_3 = client.post('/authors/', headers=headers_admin)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            "key_1": "Имя_новое",
            "key_2": "Отчество_новое",
            "key_3": "Фамилия_новая"
        }
        response_4 = client.post('/authors/', json=data_4, headers=headers_admin)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Пустые значения
        data_5 = {
            "first_name": "",
            "middle_name": "",
            "last_name": None
        }
        response_5 = client.post('/authors/', json=data_5, headers=headers_admin)
        assert response_5.status_code == 400, f'Возвращается код {response_5.status_code} вместо 400'

    def test_get_author_exceptions(self, client, author_1, headers_user):
        # Неавторизованный пользователь
        response_1 = client.get(f'/authors/{author_1.id}')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Несуществующий автор
        response_2 = client.get('/authors/2', headers=headers_user)
        assert response_2.status_code == 404, f'Возвращается код {response_2.status_code} вместо 404'

    def test_put_exceptions(self, client, author_1, headers_user, headers_admin):
        # Обращение не администратора
        response_1 = client.put(f'/authors/{author_1.id}', headers=headers_user)
        assert response_1.status_code == 403, f'Возвращается код {response_1.status_code} вместо 403'

        # Обращение без токена
        response_2 = client.put(f'/authors/{author_1.id}')
        assert response_2.status_code == 401, f'Возвращается код {response_2.status_code} вместо 401'

        # Обращение без данных
        response_3 = client.put(f'/authors/{author_1.id}', headers=headers_admin)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            "key_1": "Имя_новое",
            "key_2": "Отчество_новое",
            "key_3": "Фамилия_новая"
        }
        response_4 = client.put(f'/authors/{author_1.id}', json=data_4, headers=headers_admin)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Несуществующий автор
        data_5 = {
            "first_name": "Имя_новое",
            "middle_name": "Отчество_новое",
            "last_name": "Фамилия_новая"
        }
        response_5 = client.put('/authors/2', json=data_5, headers=headers_admin)
        assert response_5.status_code == 404, f'Возвращается код {response_5.status_code} вместо 404'

    def test_patch_exceptions(self, client, author_1, headers_user, headers_admin):
        # Обращение не администратора
        response_1 = client.patch(f'/authors/{author_1.id}', headers=headers_user)
        assert response_1.status_code == 403, f'Возвращается код {response_1.status_code} вместо 403'

        # Обращение без токена
        response_2 = client.patch(f'/authors/{author_1.id}')
        assert response_2.status_code == 401, f'Возвращается код {response_2.status_code} вместо 401'

        # Обращение без данных
        response_3 = client.patch(f'/authors/{author_1.id}', headers=headers_admin)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Несуществующий автор
        data_5 = {
            "first_name": "Имя_новое",
            "middle_name": "Отчество_новое"
        }
        response_5 = client.patch('/authors/2', json=data_5, headers=headers_admin)
        assert response_5.status_code == 404, f'Возвращается код {response_5.status_code} вместо 404'

    def test_delete_exceptions(self, author_1, client, headers_user, headers_admin):
        # Обращение не администратора
        response_1 = client.delete(f'/authors/{author_1.id}', headers=headers_user)
        assert response_1.status_code == 403, f'Возвращается код {response_1.status_code} вместо 403'

        # Обращение без токена
        response_2 = client.delete(f'/authors/{author_1.id}')
        assert response_2.status_code == 401, f'Возвращается код {response_2.status_code} вместо 401'

        # Несуществующий автор
        response_3 = client.delete('/authors/2', headers=headers_admin)
        assert response_3.status_code == 404, f'Возвращается код {response_3.status_code} вместо 404'
