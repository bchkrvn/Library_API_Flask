class TestNewsViews:
    def test_get_all_news(self, client, news_1, news_2, headers_user):
        response = client.get('/news/', headers=headers_user)
        assert response.status_code == 200, f'Вернулся статус {response.status_code} вместо 200'

        news = response.json
        news_keys = {"id", "user", "text", "amount_comments", "date", "update_date", "comments"}

        assert news is not None, 'Возвращается None или пустой список'
        assert type(news) is list, f'Возвращается {type(news)} вместо list'
        assert type(news[0]) is dict, f'В списке находятся {type(news[0])} вместо dict'
        assert news_keys == set(news[0].keys()), f'Ключи не совпадают'

    def test_post_news(self, client, user_1, headers_user, news_service):
        data = {
            "text": "new_text"
        }
        response = client.post('/news/', json=data, headers=headers_user)
        assert response.status_code == 201, f'Вернулся статус {response.status_code} вместо 201'

        news = news_service.get_all()[-1]
        assert news is not None, f'Вместо новости вернулся None'
        assert news.text == data.get('text'), 'Неверно установлен текст'
        assert news.date is not None, 'Дата публикации не установлена'
        assert news.update_date is None, "Установилась дата обновления"
        assert news.user_id == user_1.id, 'Неверный id автора'
        assert news.amount_comments == 0, "Не установлено количество комментариев"

    def test_get_one_news(self, client, news_1, comment_1, headers_user):
        response = client.get(f'/news/{news_1.id}', headers=headers_user)
        assert response.status_code == 200, f'Вернулся статус {response.status_code} вместо 200'

        news = response.json
        news_keys = {"id", "user", "text", "amount_comments", "date", "update_date", "comments"}

        assert news is not None, 'Возвращается None или пустой список'
        assert type(news) is dict, f'Возвращается {type(news)} вместо dict'
        assert news_keys == set(news.keys()), f'Ключи не совпадают'

    def test_post_comments(self, client, news_1, user_1, headers_user, comment_service):
        data = {
            "text": "new_text"
        }
        response = client.post(f'/news/{news_1.id}', json=data, headers=headers_user)
        assert response.status_code == 201, f'Вернулся статус {response.status_code} вместо 201'

        comment = comment_service.get_all()[-1]
        assert comment is not None, 'Комментарий не создался'
        assert comment.text == data.get('text'), 'Неверно установлен текс комментария'
        assert comment.date is not None, 'Не установлено время публикации'
        assert comment.update_date is None, 'Установилось время обновления'
        assert comment.user_id == user_1.id, 'Неверно установлен id пользователя'
        assert news_1.amount_comments == 1, 'В счетчик не добавился комментарий'

    def test_put_news_by_user(self, client, news_1, user_1, headers_user, news_service):
        data = {
            "text": "new_text"
        }
        response = client.put(f'/news/{news_1.id}', json=data, headers=headers_user)
        assert response.status_code == 204, f'Вернулся статус {response.status_code} вместо 204'

        news = news_service.get_one(news_1.id)
        assert news is not None, f'Вместо новости вернулся None'
        assert news.text == data.get('text'), 'Неверно установлен текст'
        assert news.date is not None, 'Дата публикации не установлена'
        assert news.update_date is not None, "Установилась дата обновления"
        assert news.date != news.update_date, 'Дата создания совпадает с датой обновления'
        assert news.date < news.update_date, 'Дата создания больше даты обновления'
        assert news.user_id == user_1.id, 'Неверный id автора'
        assert news.amount_comments == 0, "Не установлено количество комментариев"

    def test_put_news_by_admin(self, client, news_1, user_1, headers_admin, news_service):
        data = {
            "text": "new_text"
        }
        response = client.put(f'/news/{news_1.id}', json=data, headers=headers_admin)
        assert response.status_code == 204, f'Вернулся статус {response.status_code} вместо 204'

        news = news_service.get_one(news_1.id)
        assert news is not None, f'Вместо новости вернулся None'
        assert news.text == data.get('text'), 'Неверно установлен текст'
        assert news.date is not None, 'Дата публикации не установлена'
        assert news.update_date is not None, "Установилась дата обновления"
        assert news.date != news.update_date, 'Дата создания совпадает с датой обновления'
        assert news.date < news.update_date, 'Дата создания больше даты обновления'
        assert news.user_id == user_1.id, 'Неверный id автора'
        assert news.amount_comments == 0, "Не установлено количество комментариев"

    def test_delete_news_by_user(self, client, news_1, comment_1, headers_user, news_service, comment_service):
        response = client.delete(f'/news/{news_1.id}', headers=headers_user)
        assert response.status_code == 204, f'Вернулся статус {response.status_code} вместо 204'

        news = news_service.get_all()
        assert len(news) == 0, 'Новость не удалилась'

        comment = comment_service.get_all()
        assert len(comment) == 0, 'Комментарий не удалился'

    def test_delete_news_by_admin(self, client, news_1, comment_1, headers_admin, news_service, comment_service):
        response = client.delete(f'/news/{news_1.id}', headers=headers_admin)
        assert response.status_code == 204, f'Вернулся статус {response.status_code} вместо 204'

        news = news_service.get_all()
        assert len(news) == 0, 'Новость не удалилась'

        comment = comment_service.get_all()
        assert len(comment) == 0, 'Комментарий не удалился'
