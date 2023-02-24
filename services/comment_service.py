import datetime
from flask import abort

from dao.comment_dao import CommentDAO
from dao.models.models_dao import Comment
from services.news_service import NewsService
from services.users_service import UserService


class CommentService:
    def __init__(self, comment_dao: CommentDAO, news_service: NewsService, user_service: UserService):
        self.comment_dao = comment_dao
        self.news_service = news_service
        self.user_service = user_service

    def get_by_news_id(self, n_id):
        return self.comment_dao.get_by_news_id(n_id)

    def create(self, data):
        news = self.news_service.get_one(data['news_id'])
        data['user_id'] = self.user_service.get_user_from_token().id
        data['data'] = datetime.datetime.now()
        new_comment = Comment(**data)
        self.comment_dao.save(new_comment)

    def update(self, data):
        comment = self.comment_dao.get_one(data['id'])
        user = self.user_service.get_user_from_token()
        if comment.user_id != user.id and user.role != 'admin':
            abort(403)
        comment.text = data.get('text')
        comment.data = datetime.datetime.now()
        self.comment_dao.save(comment)

    def delete(self, id_):
        comment = self.comment_dao.get_one(id_)
        user = self.user_service.get_user_from_token()
        if comment.user_id != user.id and user.role != 'admin':
            abort(403)
        self.comment_dao.delete(comment)

