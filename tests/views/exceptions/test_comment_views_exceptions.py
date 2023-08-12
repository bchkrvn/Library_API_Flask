class TestCommentViewsExceptions:
    url = '/comments/'

    def test_put_comment_exceptions(self, client, comment_1, comment_2, headers_user, comment_service):
        # Обращение без токена
        response_1 = client.put(f'{self.url}{comment_1.id}/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не автора комментария
        data_2 = {
            "text": "New_text"
        }
        response_2 = client.put(f'{self.url}{comment_2.id}/', json=data_2, headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Обращение без данных
        response_3 = client.put(f'{self.url}{comment_1.id}/', headers=headers_user)
        assert response_3.status_code == 400, f'Возвращается код {response_3.status_code} вместо 400'

        # Обращение с неверным ключами
        data_4 = {
            "wrong_key": "text"
        }
        response_4 = client.put(f'{self.url}{comment_1.id}/', json=data_4, headers=headers_user)
        assert response_4.status_code == 400, f'Возвращается код {response_4.status_code} вместо 400'

        # Обращения с пустыми данными
        data_5 = {
            "text": None
        }
        response_5 = client.put(f'{self.url}{comment_1.id}/', json=data_5, headers=headers_user)
        assert response_5.status_code == 400, f'Возвращается код {response_5.status_code} вместо 400'

        data_6 = {
            "text": ""
        }
        response_6 = client.put(f'{self.url}{comment_1.id}/', json=data_6, headers=headers_user)
        assert response_6.status_code == 400, f'Возвращается код {response_6.status_code} вместо 400'

        # Несуществующий комментарий
        data_7 = {
            "text": "comment"
        }
        response_7 = client.put(f'{self.url}999999/', json=data_7, headers=headers_user)
        assert response_7.status_code == 404, f'Возвращается код {response_7.status_code} вместо 404'

    def test_delete_exceptions(self, client, comment_1, comment_2, headers_admin, user_2, headers_user):
        # Обращение без токена
        response_1 = client.put(f'{self.url}{comment_1.id}/')
        assert response_1.status_code == 401, f'Возвращается код {response_1.status_code} вместо 401'

        # Обращение не автора комментария
        response_2 = client.delete(f'{self.url}{comment_2.id}/', headers=headers_user)
        assert response_2.status_code == 403, f'Возвращается код {response_2.status_code} вместо 403'

        # Несуществующий комментарий
        response_2 = client.delete(f'{self.url}999999/', headers=headers_user)
        assert response_2.status_code == 404, f'Возвращается код {response_2.status_code} вместо 404'
