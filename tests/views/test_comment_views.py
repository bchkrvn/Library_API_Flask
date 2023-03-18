class TestCommentViews:
    def test_put_comment(self, client, comment_1, headers_user, headers_admin, comment_service):
        # Изменение пользователем
        data_1 = {
            "text": "new_text_by_user"
        }
        response_1 = client.put(f'/comments/{comment_1.id}', json=data_1, headers=headers_user)
        assert response_1.status_code == 204, f'Вернулся статус {response_1.status_code} вместо 204'

        comment_user = comment_service.get_one(comment_1.id)
        assert comment_user is not None, 'Вместо комментария вернулся None'
        assert comment_user.text == data_1.get('text'), 'Текст комментария не обновлен'
        assert comment_user.update_date is not None, 'Не установлена дата обновления'
        assert comment_user.update_date != comment_user.date, 'Дата создания совпадает с датой обновления'

        # Изменение администратором
        data_2 = {
            "text": "new_text_by_admin"
        }
        response = client.put(f'/comments/{comment_1.id}', json=data_2, headers=headers_admin)
        assert response.status_code == 204, f'Вернулся статус {response.status_code} вместо 204'

        comment_admin = comment_service.get_one(comment_1.id)
        assert comment_admin is not None, 'Вместо комментария вернулся None'
        assert comment_admin.text == data_2.get('text'), 'Текст комментария не обновлен'
        assert comment_admin.update_date is not None, 'Не установлена дата обновления'
        assert comment_admin.update_date != comment_admin.date, 'Дата создания совпадает с датой обновления'

    def test_delete(self, client, comment_1, comment_2, headers_user, news_1, headers_admin, comment_service):
        # Удаление пользователем
        response = client.delete(f'/comments/{comment_1.id}', headers=headers_user)
        assert response.status_code == 204, f'Вернулся статус {response.status_code} вместо 204'

        comments = comment_service.get_all()
        assert len(comments) == 1, 'Комментарий не удален'

        # Удаление администратором
        response = client.delete(f'/comments/{comment_2.id}', headers=headers_admin)
        assert response.status_code == 204, f'Вернулся статус {response.status_code} вместо 204'

        comments = comment_service.get_all()
        assert len(comments) == 0, 'Комментарий не удален'
