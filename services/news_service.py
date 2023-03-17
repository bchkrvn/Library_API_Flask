import datetime

from flask import abort

from dao.comment_dao import CommentDAO
from dao.models.models_dao import News
from dao.news_dao import NewsDAO
from services.users_service import UserService


class NewsService:
    def __init__(self, news_dao: NewsDAO, user_service: UserService, comment_dao: CommentDAO):
        self.news_dao = news_dao
        self.user_service = user_service
        self.comment_dao = comment_dao

    def get_all(self):
        return self.news_dao.get_all()

    def get_one(self, n_id):
        news = self.news_dao.get_one(n_id)
        if not news:
            abort(404, f'News id = {n_id} not found')
        return news

    def create(self, data):
        data['data'] = datetime.datetime.now()
        new_news = News(**data)
        self.news_dao.save(new_news)

    def update(self, data):
        news = self.get_one(data['n_id'])
        user = self.user_service.get_one(data['u_id'])

        if news.user_id != user.id and user.role != 'admin':
            abort(403)

        news.text = data.get('text')
        news.data = datetime.datetime.now()
        self.news_dao.save(news)

    def delete(self, n_id, u_id):
        news = self.get_one(n_id)
        user = self.user_service.get_one(u_id)

        if news.user_id != user.id and user.role != 'admin':
            abort(403)

        self.news_dao.delete(news)
        self.comment_dao.delete_by_news_id(n_id)

    def add_comments_to_amount(self, news):
        news.amount_comments += 1
        self.news_dao.save(news)

    def remove_comments_to_amount(self, news):
        news.amount_comments -= 1
        self.news_dao.save(news)
