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