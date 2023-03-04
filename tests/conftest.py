from datetime import datetime

import pytest as pytest

from app import create_app
from config import TestingConfig
from dao.authors_dao import AuthorDAO
from dao.books_dao import BookDAO
from dao.comment_dao import CommentDAO
from dao.models.models_dao import Author, Book, Reader, User, News, Comment
from dao.news_dao import NewsDAO
from dao.readers_dao import ReaderDAO
from dao.users_dao import UserDAO
from setup_db import db as database
from tools.security import get_hash


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        yield app


@pytest.fixture
def db(app):
    database.init_app(app)
    database.drop_all()
    database.create_all()
    database.session.commit()

    yield database

    database.session.close()


@pytest.fixture
def client(app, db):
    with app.test_client() as client:
        yield client


"""Тестовые DAO"""


@pytest.fixture
def author_dao(db):
    return AuthorDAO(db.session)


@pytest.fixture
def book_dao(db):
    return BookDAO(db.session)


@pytest.fixture
def reader_dao(db):
    return ReaderDAO(db.session)


@pytest.fixture
def user_dao(db):
    return UserDAO(db.session)


@pytest.fixture
def news_dao(db):
    return NewsDAO(db.session)


@pytest.fixture
def comment_dao(db):
    return CommentDAO(db.session)


"""Тестовые объекты"""


@pytest.fixture
def author_1(db):
    a = Author(
        first_name='Имя_1',
        middle_name="Отчество_1",
        last_name="Фамилия_1"
    )
    db.session.add(a)
    db.session.commit()
    return a


@pytest.fixture
def author_2(db):
    a = Author(
        first_name='Имя_2',
        middle_name="Отчество_2",
        last_name="Фамилия_2"
    )
    db.session.add(a)
    db.session.commit()
    return a


@pytest.fixture
def book_1(db):
    b = Book(
        title='Название_1',
        is_in_lib=True,
        author_id=1,
        reader_id=1,
    )
    db.session.add(b)
    db.session.commit()
    return b


@pytest.fixture
def book_2(db):
    b = Book(
        title='Название_2',
        is_in_lib=False,
        author_id=2,
        reader_id=2,
    )
    db.session.add(b)
    db.session.commit()
    return b


@pytest.fixture
def reader_1(db):
    r = Reader(
        first_name='Имя_1',
        last_name='Фамилия_1',
        user_id=1
    )
    db.session.add(r)
    db.session.commit()
    return r


@pytest.fixture
def reader_2(db):
    r = Reader(
        first_name='Имя_2',
        last_name='Фамилия_2',
        user_id=1
    )
    db.session.add(r)
    db.session.commit()
    return r


@pytest.fixture
def user_1(db):
    password = get_hash('1111')
    u = User(
        username='name_1',
        password=password,
        role='user'
    )
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def user_2(db):
    password = get_hash('2222')
    u = User(
        username='name_2',
        password=password,
        role='user'
    )
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def admin(db):
    password = get_hash('1111')
    a = User(
        username='name_1',
        password=password,
        role='admin'
    )
    db.session.add(a)
    db.session.commit()
    return a


@pytest.fixture
def news_1(db):
    n = News(
        user_id=1,
        text='Текст_1',
        data=datetime.now()
    )
    db.session.add(n)
    db.session.commit()
    return n


@pytest.fixture
def news_2(db):
    n = News(
        user_id=2,
        text='Текст_2',
        data=datetime.now()
    )
    db.session.add(n)
    db.session.commit()
    return n


@pytest.fixture
def comment_1(db):
    c = Comment(
        news_id=1,
        user_id=1,
        text='Текст_1',
        data=datetime.now(),
    )
    db.session.add(c)
    db.session.commit()
    return c


@pytest.fixture
def comment_2(db):
    c = Comment(
        news_id=1,
        user_id=2,
        text='Текст_2',
        data=datetime.now(),
    )
    db.session.add(c)
    db.session.commit()
    return c
