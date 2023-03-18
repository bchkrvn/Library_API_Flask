class TestAuthViews:
    def test_post(self, client, user_1):
        data = {
            "username": user_1.username,
            "password": "1111"
        }
        response = client.post('/auth/', json=data)
        assert response.status_code == 200, f'Возвращается статус {response.status_code} вместо 200'

        tokens = response.json
        assert type(tokens) is dict, f'Возвращается не словарь, а {type(tokens)}'
        assert len(tokens) == 2, f'Возвращается {len(tokens)} элементов, ожидалось 2 '
        assert 'access_token' in tokens, f'В токенах нет access_token'
        assert 'refresh_token' in tokens, f'В токенах нет refresh_token'
        assert None not in tokens.values(), f'Вместо токенов возвращается None'

    def test_put(self, client, user_1, headers_user):
        data = {
            "username": user_1.username,
            "password": "1111"
        }
        response_post = client.post('/auth/', json=data)
        assert response_post.status_code == 200, f'Возвращается статус {response_post.status_code} вместо 200'

        tokens = response_post.json
        del tokens['access_token']

        response_put = client.put('/auth/', json=tokens)
        assert response_put.status_code == 200, f'Возвращается статус {response_put.status_code} вместо 200'

        new_tokens = response_put.json
        assert type(new_tokens) is dict, f'Возвращается не словарь, а {type(new_tokens)}'
        assert len(new_tokens) == 2, f'Возвращается {len(new_tokens)} элементов, ожидалось 2 '
        assert 'access_token' in new_tokens, f'В токенах нет access_token'
        assert 'refresh_token' in new_tokens, f'В токенах нет refresh_token'
        assert None not in new_tokens.values(), f'Вместо токенов возвращается None'
