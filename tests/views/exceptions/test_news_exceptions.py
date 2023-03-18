class TestNewsViewsExceptions:
    def test_get_all_news_exceptions(self, client, news_1, headers_user):
        # Неавторизованный пользователь
        response = client.get('/news/')
        assert response.status_code == 401, f'Возвращается код {response.status_code} вместо 401'

    def test_post_news_exceptions(self, client, headers_user):
        # Неавторизованный пользователь
        response_1 = client.post('/news/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение без данных
        response_2 = client.post('/news/', headers=headers_user)
        assert response_2.status_code == 400, f'Возвращается код {response_2.status_code} вместо 400'

        # Неверные ключи
        data_3 = {
            "wrong_key": "data"
        }
        response_3 = client.post('/news/', json=data_3, headers=headers_user)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Пустые значения
        data_4 = {
            "text": None
        }
        response_4 = client.post('/news/', json=data_4, headers=headers_user)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        data_5 = {
            "text": ""
        }
        response_5 = client.post('/news/', json=data_5, headers=headers_user)
        assert response_5.status_code == 400, f'Возвращается код {response_5.status_code} вместо 400'

    def test_get_one_exceptions(self, client, news_1, headers_user):
        # Неавторизованный пользователь
        response_1 = client.get(f'/news/{news_1.id}')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Несуществующая новость
        response_2 = client.get(f'/news/99999', headers=headers_user)
        assert response_2.status_code == 404, f'Возвращается код {response_2.status_code} вместо 404'

    def test_post_comment_exceptions(self, client, news_1, headers_user):
        # Неавторизованный пользователь
        response_1 = client.post(f'/news/{news_1.id}')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Несуществующая новость
        data_2 = {
            'text': 'new_comment'
        }
        response_2 = client.post(f'/news/99999', json=data_2, headers=headers_user)
        assert response_2.status_code == 404, f'Возвращается код {response_2.status_code} вместо 404'

        # Обращение без данных
        response_3 = client.post(f'/news/{news_1.id}', headers=headers_user)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            "wrong_key": "data"
        }
        response_4 = client.post(f'/news/{news_1.id}', json=data_4, headers=headers_user)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Пустые значения
        data_5 = {
            "text": None
        }
        response_5 = client.post(f'/news/{news_1.id}', json=data_5, headers=headers_user)
        assert response_5.status_code == 400, f'Возвращается код {response_5.status_code} вместо 400'

        data_6 = {
            "text": ""
        }
        response_6 = client.post(f'/news/{news_1.id}', json=data_6, headers=headers_user)
        assert response_6.status_code == 400, f'Возвращается код {response_6.status_code} вместо 400'

    def test_put_news_exceptions(self, client, news_1, news_2, user_1, user_2, headers_user):
        # Неавторизованный пользователь
        response_1 = client.put(f'/news/{news_1.id}')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Несуществующая новость
        data_2 = {
            'text': 'new_comment'
        }
        response_2 = client.put(f'/news/99999', json=data_2, headers=headers_user)
        assert response_2.status_code == 404, f'Возвращается код {response_2.status_code} вместо 404'

        # Обращение без данных
        response_3 = client.put(f'/news/{news_1.id}', headers=headers_user)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Неверные ключи
        data_4 = {
            "wrong_key": "data"
        }
        response_4 = client.put(f'/news/{news_1.id}', json=data_4, headers=headers_user)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Пустые значения
        data_5 = {
            "text": None
        }
        response_5 = client.put(f'/news/{news_1.id}', json=data_5, headers=headers_user)
        assert response_5.status_code == 400, f'Возвращается код {response_5.status_code} вместо 400'

        data_6 = {
            "text": ""
        }
        response_6 = client.put(f'/news/{news_1.id}', json=data_6, headers=headers_user)
        assert response_6.status_code == 400, f'Возвращается код {response_6.status_code} вместо 400'

        # Обращение не автора новости
        data_7 = {
            'text': 'new_comment'
        }
        response_7 = client.put(f'/news/{news_2.id}', json=data_7, headers=headers_user)
        assert response_7.status_code == 403, f'Возвращается код {response_7.status_code} вместо 403'

    def test_delete_news_exceptions(self, client, news_1, news_2, headers_user):
        # Неавторизованный пользователь
        response_1 = client.delete(f'/news/{news_1.id}')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Несуществующая новость
        response_2 = client.delete(f'/news/99999', headers=headers_user)
        assert response_2.status_code == 404, f'Возвращается код {response_2.status_code} вместо 404'

        # Обращение не автора новости
        response_3 = client.delete(f'/news/{news_2.id}', headers=headers_user)
        assert response_3.status_code == 403, f'Возвращается код {response_3.status_code} вместо 403'
