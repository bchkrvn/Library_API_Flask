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

    def get_one(self, c_id):
        comment = self.comment_dao.get_one(c_id)
        if not comment:
            abort(404, f'comment id={c_id} not found')
        return comment

    def get_all(self):
        return self.comment_dao.get_all()

    def create(self, data):
        news = self.news_service.get_one(data['news_id'])

        data['date'] = datetime.datetime.now()
        new_comment = Comment(**data)
        self.comment_dao.save(new_comment)
        self.news_service.add_comments_to_amount(news)

    def update(self, data):
        comment = self.get_one(data['id'])
        user = self.user_service.get_one(data['user_id'])

        if comment.user_id != user.id and user.role != 'admin':
            abort(403)

        comment.text = data.get('text')
        comment.update_date = datetime.datetime.now()
        self.comment_dao.save(comment)

    def delete(self, c_id, u_id):
        comment = self.get_one(c_id)
        user = self.user_service.get_one(u_id)
        news = self.news_service.get_one(comment.news_id)

        if comment.user_id != user.id and user.role != 'admin':
            abort(403, "You don't have access")

        self.comment_dao.delete(comment)
        self.news_service.remove_comments_to_amount(news)

    def delete_by_news_id(self, n_id):
        self.comment_dao.delete_by_news_id(n_id)
