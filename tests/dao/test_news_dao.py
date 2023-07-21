from datetime import datetime

from app.dao.models.models_dao import News


class TestNewsDAO:
    def test_get_all(self, news_1, news_2, news_dao):
        news = news_dao.get_all()

        assert news is not None, "Возвращается None вместо книг"
        assert type(news) is list, 'Возвращается не список'
        assert len(news) == 2, f'Возвращается больше книг({len(news)}), чем ожидалось(2)'
        assert news_1 in news, "Первой книги нет в списке"
        assert news_2 in news, "Второй книги нет в списке"

    def test_get_one(self, news_1, news_dao):
        news = news_dao.get_one(news_1.id)

        assert news is not None, "Возвращается None вместо новости"
        assert type(news) is News, f'Возвращается не новость, а {type(news)}'
        assert news.id == news_1.id, "id новости не совпадает"
        assert news.user_id == news_1.user_id, "user_id новости не совпадает"
        assert news.text == news_1.text, "text новости не совпадает"
        assert news.date == news_1.date, "data новости не совпадает"
        assert news.update_date == news_1.update_date, "data обновления новости не совпадает"

    def test_save(self, news_dao):
        news_1 = News(
            user_id=1,
            text='Текст_1',
            date=datetime.now()
        )
        news_dao.save(news_1)
        news = news_dao.get_one(news_1.id)

        assert news is not None, "Возвращается None вместо новости"
        assert type(news) is News, f'Возвращается не новость, а {type(news)}'
        assert news.id == news_1.id, "id новости не совпадает"
        assert news.user_id == news_1.user_id, "user_id новости не совпадает"
        assert news.text == news_1.text, "text новости не совпадает"
        assert news.date == news_1.date, "data новости не совпадает"
        assert news.update_date == news_1.update_date, "data новости не совпадает"

    def test_delete(self, news_1, news_dao):
        news_dao.delete(news_1)
        news = news_dao.get_all()

        assert len(news) == 0, 'Новость не удалена'
        