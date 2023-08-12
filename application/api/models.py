from flask_restx import fields, Model

from api.api import api

author: Model = api.model('Автор', {
    'id': fields.Integer(required=True, example=1),
    'first_name': fields.String(required=True, example='Иван'),
    'middle_name': fields.String(required=True, example='Иванович'),
    'last_name': fields.String(required=True, example='Иванов'),
})

user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'username': fields.String(required=True, example=1),
})

reader: Model = api.model('Читатель', {
    'id': fields.Integer(required=True, example=1),
    'first_name': fields.String(example='Иван'),
    'last_name': fields.String(example='Иванов'),
    'user': fields.Nested(user)
})

book: Model = api.model('Книга', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, example='Сказки'),
    'is_in_lib': fields.Boolean(required=True, example='True'),
    'author': fields.Nested(author),
    'reader': fields.Nested(reader, allow_null=True),
})

comment: Model = api.model('Комментарий', {
    'id': fields.Integer(required=True, example=1),
    'news_id': fields.Integer(required=True, example=1),
    'user': fields.Nested(user),
    'text': fields.String(required=True, example='Текст комментария'),
    'date': fields.DateTime(required=True, example='2000-01-01 00:00:00.000000'),
    'update_date': fields.DateTime(required=False, example='2000-01-01 00:00:00.000000')
})

news: Model = api.model('Новость', {
    'id': fields.Integer(required=True, example=1),
    'user': fields.Nested(user),
    'text': fields.String(required=True, max_length=255, example='Текст новости'),
    'amount_comments': fields.Integer(required=True, example=1),
    'comments': fields.List(fields.Nested(comment)),
    'date': fields.DateTime(required=True, example='2000-01-01 00:00:00.000000'),
    'update_date': fields.DateTime(required=False, example='2000-01-01 00:00:00.000000')
})
