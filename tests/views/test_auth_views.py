import json

import pytest
from werkzeug.exceptions import BadRequest, NotFound


class TestAuthViews:
    def test_post(self, client, user_1):
        data = {
            "username": user_1.username,
            "password": "1111"
        }
        response = client.post('/auth/', json=data)

        tokens = response.json
        assert response.status_code == 200, f'Возвращается статус {response.status_code} вместо 200'
        assert type(tokens) is dict, f'Возвращается не словарь, а {type(tokens)}'
        assert len(tokens) == 2, f'Возвращается {len(tokens)} элементов, ожидалось 2 '
        assert 'access_token' in tokens, f'В токенах нет access_token'
        assert 'refresh_token' in tokens, f'В токенах нет refresh_token'
        assert None not in tokens.values(), f'Вместо токенов возвращается None'

    def test_post_exceptions(self, client, user_1):
        # Пустой запрос пользователь
        response_1 = client.post('/auth/')
        assert response_1.status_code == 400, f'Статус код - {response_1.status_code} вместо 400'

        # Нет данных в username и password
        data_2 = {
            "username": None,
            "password": None
        }
        response_2 = client.post('/auth/', json=data_2)
        assert response_2.status_code == 400, f'Статус код - {response_1.status_code} вместо 400'

        # Несуществующий пользователь
        data_3 = {
            "username": "wrong_username",
            "password": "111"
        }
        response_3 = client.post('/auth/', json=data_3)
        assert response_3.status_code == 404, f'Статус код - {response_1.status_code} вместо 404'

        # Неверный пароль
        data_4 = {
            "username": user_1.username,
            "password": "wrong_password"
        }
        response_4 = client.post('/auth/', json=data_4)
        assert response_4.status_code == 400, f'Статус код - {response_1.status_code} вместо 400'
