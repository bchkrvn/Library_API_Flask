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
from services.authors_service import AuthorService
from services.auths_service import AuthService
from services.books_service import BookService
from services.comment_service import CommentService
from services.news_service import NewsService
from services.readers_service import ReaderService
from services.users_service import UserService
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


"""Тестовые сервисы"""


@pytest.fixture
def author_service(author_dao):
    return AuthorService(author_dao)


@pytest.fixture
def reader_service(reader_dao):
    return ReaderService(reader_dao)


@pytest.fixture
def book_service(book_dao, author_service, reader_service):
    return BookService(book_dao, author_service, reader_service)


@pytest.fixture
def user_service(user_dao, reader_service):
    return UserService(user_dao, reader_service)


@pytest.fixture
def auth_service(user_service):
    return AuthService(user_service)


@pytest.fixture
def news_service(news_dao, user_service, comment_dao):
    return NewsService(news_dao, user_service, comment_dao)


@pytest.fixture
def comment_service(comment_dao, news_service, user_service):
    return CommentService(comment_dao, news_service, user_service)


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
        reader_id=None,
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
def hard_password_1():
    return 'qWer5%ty'


@pytest.fixture
def easy_password_1():
    return '1111'


@pytest.fixture
def user_1(db, hard_password_1):
    password = get_hash(hard_password_1)
    u = User(
        username='name_1',
        password=password,
        role='user'
    )
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def user_2(db, hard_password_1):
    password = get_hash(hard_password_1)
    u = User(
        username='name_2',
        password=password,
        role='user'
    )
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def admin(db, hard_password_1):
    password = get_hash(hard_password_1)
    a = User(
        username='admin',
        password=password,
        role='admin',
    )
    db.session.add(a)
    db.session.commit()
    return a


@pytest.fixture
def news_1(db):
    n = News(
        user_id=1,
        text='Текст_1',
        date=datetime.now(),
        update_date=None,
    )
    db.session.add(n)
    db.session.commit()
    return n


@pytest.fixture
def news_2(db):
    n = News(
        user_id=2,
        text='Текст_2',
        date=datetime.now(),
        update_date=None,
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
        date=datetime.now(),
        update_date=None,
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
        date=datetime.now(),
        update_date=None,
    )
    db.session.add(c)
    db.session.commit()
    return c


@pytest.fixture
def headers_user(user_1, auth_service, hard_password_1):
    tokens = auth_service.generate_token(user_1.username, hard_password_1)
    access_token = tokens['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}'}
    return headers


@pytest.fixture
def headers_admin(admin, auth_service, hard_password_1):
    tokens = auth_service.generate_token(admin.username, hard_password_1)
    access_token = tokens['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}'}
    return headers
