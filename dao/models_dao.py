from sqlalchemy.orm import relationship

from setup_db import db
from marshmallow import Schema, fields


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    is_in_lib = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = relationship('Author')
    reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'))
    reader = relationship('Reader')


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    is_in_lib = fields.Boolean()
    author_id = fields.Int()
    reader_id = fields.Int()


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str()
    middle_name = fields.Str()
    last_name = fields.Str()


class Reader(db.Model):
    __tablename__ = 'reader'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship('User')


class ReaderSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    user_id = fields.Int()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    role = db.Column(db.String)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    password = fields.Str()
    role = fields.Str()
