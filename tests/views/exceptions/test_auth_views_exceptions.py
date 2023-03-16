class TestAuthViewsExceptions:
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
