import datetime

from flask import abort

from dao.models.models_dao import News
from dao.news_dao import NewsDAO
from services.users_service import UserService


class NewsService:
    def __init__(self, news_dao: NewsDAO, user_service: UserService):
        self.news_dao = news_dao
        self.user_service = user_service

    def get_all(self):
        return self.news_dao.get_all()

    def get_one(self, n_id):
        news = self.news_dao.get_one(n_id)
        if not news:
            abort(400, f'news id={n_id} not found')

        return news

    def create(self, data):
        data['user_id'] = self.user_service.get_user_from_token().id
        data['data'] = datetime.datetime.now()
        new_news = News(**data)
        self.news_dao.save(new_news)

    def update(self, data):
        news = self.get_one(data['id'])
        user = self.user_service.get_user_from_token()
        if news.user_id != user.id and user.role != 'admin':
            abort(403)
        news.text = data.get('text')
        news.data = datetime.datetime.now()
        self.news_dao.save(news)

    def delete(self, id_):
        news = self.get_one(id_)
        user = self.user_service.get_user_from_token()
        if news.user_id != user.id and user.role != 'admin':
            abort(403)
        self.news_dao.delete(news)
