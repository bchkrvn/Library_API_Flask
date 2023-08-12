import datetime

from flask import abort

from dao.comment_dao import CommentDAO
from dao.models.models_dao import News
from dao.news_dao import NewsDAO
from services.users_service import UserService


class NewsService:
    """
    Сервис для работы с новостями
    """
    def __init__(self, news_dao: NewsDAO, user_service: UserService, comment_dao: CommentDAO):
        self.news_dao = news_dao
        self.user_service = user_service
        self.comment_dao = comment_dao

    def get_all(self) -> list[News]:
        """
        Получить список всех новостей
        :return: list[News]
        """
        return self.news_dao.get_all()

    def get_one(self, n_id: int) -> News:
        """
        Получить новость по ее id
        :param n_id: id новости
        :return: News
        """
        news = self.news_dao.get_one(n_id)
        if not news:
            abort(404, f'News id = {n_id} not found')
        return news

    def create(self, data: dict):
        """
        Создать новую новость
        :param data: данные, содержащие текст и id пользователя - автора новости
        """
        data['date'] = datetime.datetime.now()
        new_news = News(**data)
        self.news_dao.save(new_news)

    def update(self, data: dict):
        """
        Обновить текс новости
        :param data: данные, содержащие текст и id пользователя, который пытается обновить новость
        """
        news = self.get_one(data['n_id'])
        user = self.user_service.get_one(data['u_id'])

        if news.user_id != user.id and user.role != 'admin':
            abort(403)

        news.text = data.get('text')
        news.update_date = datetime.datetime.now()
        self.news_dao.save(news)

    def delete(self, n_id: int, u_id: int):
        """
        Удалить новость по ее id
        :param n_id: id новости
        :param u_id: id пользователя, который пытается удалить новость
        """
        news = self.get_one(n_id)
        user = self.user_service.get_one(u_id)

        if news.user_id != user.id and user.role != 'admin':
            abort(403)

        self.comment_dao.delete_by_news_id(n_id)
        self.news_dao.delete(news)


    def add_comments_to_amount(self, news: News):
        """
        Обновить количество комментариев у новости при создании нового комментария
        :param news: Новость, у которой добавился комментарий
        """
        news.amount_comments += 1
        self.news_dao.save(news)

    def remove_comments_from_amount(self, news: News):
        """
        Обновить количество комментариев у новости при удалении комментария
        :param news: Новость, у которой удалили комментарий
        """
        news.amount_comments -= 1
        self.news_dao.save(news)
