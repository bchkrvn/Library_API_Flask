from datetime import datetime

from application.dao.models.models_dao import Comment


class TestCommentDAO:
    def test_get_all(self, comment_1, comment_2, comment_dao):
        comments = comment_dao.get_all()

        assert comments is not None, "Возвращается None вместо комментариев"
        assert type(comments) is list, 'Возвращается не список'
        assert len(comments) == 2, f'Возвращается больше комментариев({len(comments)}), чем ожидалось(2)'
        assert comment_1 in comments, "Первого комментария нет в списке"
        assert comment_2 in comments, "Второго комментария нет в списке"

    def test_get_one(self, comment_1, comment_dao):
        comment = comment_dao.get_one(comment_1.id)

        assert comment is not None, "Возвращается None вместо комментария"
        assert type(comment) is Comment, f'Возвращается не комментарий, а {type(comment)}'
        assert comment.id == comment_1.id, "id комментария не совпадает"
        assert comment.news_id == comment_1.news_id, "news_id комментария не совпадает"
        assert comment.user_id == comment_1.user_id, "user_id комментария не совпадает"
        assert comment.text == comment_1.text, "text комментария не совпадает"
        assert comment.date == comment_1.date, "data комментария не совпадает"
        assert comment.update_date == comment_1.update_date, "data обновления комментария не совпадает"

        comment = comment_dao.get_one(2)

        assert comment is None, f'Возвращается{type(comment)} вместо None'

    def test_get_by_news_id(self, comment_1, comment_dao):
        comments = comment_dao.get_by_news_id(comment_1.news_id)

        assert comments is not None, "Возвращается None вместо комментариев"
        assert type(comments) is list, 'Возвращается не список'
        assert len(comments) == 1, f'Возвращается больше комментариев({len(comments)}), чем ожидалось(1)'
        assert comment_1 in comments, "Первого комментария нет в списке"

        comments = comment_dao.get_by_news_id(2)

        assert comments is not None, "Возвращается None вместо комментариев"
        assert type(comments) is list, 'Возвращается не список'
        assert len(comments) == 0, 'Возвращается комментарий, которого не должно быть'

    def test_save(self, comment_dao):
        comment_1 = Comment(
            news_id=1,
            user_id=1,
            text='Текст_1',
            date=datetime.now(),
        )
        comment_dao.save(comment_1)
        comment = comment_dao.get_one(comment_1.id)

        assert comment is not None, "Возвращается None вместо комментария"
        assert type(comment) is Comment, f'Возвращается не комментарий, а {type(comment)}'
        assert comment.id == comment_1.id, "id комментария не совпадает"
        assert comment.news_id == comment_1.news_id, "news_id комментария не совпадает"
        assert comment.user_id == comment_1.user_id, "user_id комментария не совпадает"
        assert comment.text == comment_1.text, "text комментария не совпадает"
        assert comment.date == comment_1.date, "data комментария не совпадает"
        assert comment.update_date == comment_1.update_date, "data обновления комментария не совпадает"

    def test_delete(self, comment_1, news_1, comment_dao):
        comment_dao.delete(comment_1)
        comments = comment_dao.get_all()

        assert len(comments) == 0, 'Комментарий не удален'

    def test_delete_by_news_id(self, comment_1, news_1, comment_dao):
        comment_dao.delete_by_news_id(news_1.id)
        comments = comment_dao.get_all()

        assert len(comments) == 0, 'Комментарий не удален'
