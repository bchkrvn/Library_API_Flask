import time

import pytest
from werkzeug.exceptions import NotFound, Forbidden

from application.dao.models.models_dao import Comment


class TestCommentService:
    def test_get_by_news_id(self, news_1, news_2, comment_1, comment_2, comment_service):
        comments = comment_service.get_by_news_id(news_1.id)

        assert comments is not None, 'Возвращается None вместо списка комментариев'
        assert type(comments) is list, 'Возвращается не список'
        assert len(comments) == 2, 'Возвращается не два комментария'
        assert comment_1 in comments, 'Первый комментарий не возвращается'
        assert comment_2 in comments, 'Второй комментарий не возвращается'

        comments = comment_service.get_by_news_id(news_2.id)

        assert comments is not None, 'Возвращается None вместо списка комментариев'
        assert type(comments) is list, 'Возвращается не список'
        assert len(comments) == 0, 'Возвращаются комментарии к новости, у которой их нет'

    def test_get_one(self, comment_1, comment_service):
        comment = comment_service.get_one(comment_1.id)

        assert comment is not None, 'Возвращается None вместо комментария'
        assert type(comment) is Comment, 'Возвращается не комментарий'
        assert comment.news_id == comment_1.news_id, 'Неверный id новости'
        assert comment.user_id == comment_1.user_id, 'Неверный id пользователя'
        assert comment.text == comment_1.text, 'Неверный текст'
        assert comment.date == comment_1.date, 'Неверная дата'
        assert comment.update_date == comment_1.update_date, 'Неверная дата обновления'

        with pytest.raises(NotFound):
            comment_service.get_one(2)

    def test_create(self, news_1, user_1, comment_service):
        data = {
            'news_id': news_1.id,
            'user_id': user_1.id,
            'text': 'text_1',
        }
        comment_service.create(data)
        comment = comment_service.get_one(1)

        assert type(comment) is Comment, 'Возвращается не комментарий'
        assert comment.news_id == data.get('news_id'), 'Неверный id новости'
        assert comment.user_id == data.get('user_id'), 'Неверный id пользователя'
        assert comment.text == data.get('text'), 'Неверный текст'
        assert comment.date is not None, 'Нет времени и даты'
        assert news_1.amount_comments == 1, 'Количество комментариев у новости не изменилось'

    def test_create_errors(self, news_1, user_1, comment_service):
        # Неверный id новости
        with pytest.raises(NotFound):
            data = {
                'news_id': 2,
                'user_id': user_1.id,
                'text': 'text_1'
            }
            comment_service.create(data)

    def test_update(self, user_1, admin, comment_1, comment_service):
        # Обновление пользователем
        data = {
            'id': comment_1.id,
            'user_id': user_1.id,
            'text': 'text_1',
        }
        time.sleep(0.001)
        comment_service.update(data)
        comment = comment_service.get_one(comment_1.id)

        assert comment.text == data.get('text'), 'Текст комментария не обновился'
        assert comment.update_date is not None, 'Дата и время обновления комментария не установилась'
        assert comment.update_date != comment.date, 'Дата и время обновления комментария совпадает с временем создания'

        # Обновление администратором
        data = {
            'id': comment_1.id,
            'user_id': admin.id,
            'text': 'text_2',
        }
        time.sleep(0.001)
        comment_service.update(data)
        comment = comment_service.get_one(comment_1.id)

        assert comment.text == data.get('text'), 'Текст комментария не обновился'
        assert comment.update_date is not None, 'Дата и время обновления комментария не установилась'
        assert comment.update_date != comment.date, 'Дата и время обновления комментария совпадает с временем создания'

    def test_update_errors(self, user_1, user_2, comment_1, comment_service):
        # Несуществующий пользователь
        with pytest.raises(NotFound):
            data = {
                'id': comment_1.id,
                'user_id': 3,
                'text': 'text_1',
            }
            comment_service.update(data)

        # Несуществующий комментарий
        with pytest.raises(NotFound):
            data = {
                'id': 2,
                'user_id': user_1.id,
                'text': 'text_1',
            }
            comment_service.update(data)

        # Неверный пользователь
        with pytest.raises(Forbidden):
            data = {
                'id': comment_1.id,
                'user_id': user_2.id,
                'text': 'text_1',
            }
            comment_service.update(data)

    def test_delete_by_user(self, comment_1, user_1, news_1, comment_service):
        comment_service.delete(comment_1.id, user_1.id)
        comments = comment_service.get_by_news_id(1)

        assert len(comments) == 0, 'Комментарий не удалился'
        assert news_1.amount_comments == -1, 'Количество комментариев у новости не изменилось'

    def test_delete_by_admin(self, comment_1, user_1, admin, news_1, comment_service):
        comment_service.delete(comment_1.id, admin.id)
        comments = comment_service.get_by_news_id(1)

        assert len(comments) == 0, 'Комментарий не удалился'
        assert news_1.amount_comments == -1, 'Количество комментариев у новости не изменилось'

    def test_delete_errors(self, comment_1, user_1, user_2, news_1, comment_service):
        # Несуществующий комментарий
        with pytest.raises(NotFound):
            comment_service.delete(2, user_1.id)

        # Несуществующий пользователь
        with pytest.raises(NotFound):
            comment_service.delete(comment_1.id, 3)

        # Удаляет не тот пользователь
        with pytest.raises(Forbidden):
            comment_service.delete(comment_1.id, user_2.id)
