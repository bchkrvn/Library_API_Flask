from sqlalchemy.orm import relationship

from setup_db import db
from marshmallow import Schema, fields


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    is_in_lib = db.Column(db.Boolean, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = relationship('Author')
    reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'))
    reader = relationship('Reader')


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)


class Reader(db.Model):
    __tablename__ = 'reader'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User')


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    role = db.Column(db.String)


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    text = db.Column(db.String(255), nullable=False)
    amount_comments = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, nullable=False)
    update_date = db.Column(db.DateTime)


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()


class NewsSchema(Schema):
    id = fields.Int(dump_only=True)
    user = fields.Nested(UserSchema)
    text = fields.Str()
    date = fields.DateTime()
    amount_comments = fields.Integer()
    update_date = fields.DateTime()


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    news = relationship('News')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    text = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    update_date = db.Column(db.DateTime)


class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    news_id = fields.Int()
    user = fields.Nested(UserSchema)
    text = fields.Str()
    date = fields.DateTime()
    update_date = fields.DateTime()
