from app.dao.authors_dao import AuthorDAO
from app.dao import BookDAO
from app.dao.comment_dao import CommentDAO
from app.dao.news_dao import NewsDAO
from app.dao.readers_dao import ReaderDAO
from app.dao.users_dao import UserDAO
from app.services.authors_service import AuthorService
from app.services.auths_service import AuthService
from app.services.books_service import BookService
from app.services import CommentService
from app.services.news_service import NewsService
from app.services.readers_service import ReaderService
from app.services.users_service import UserService
from setup_db import db

reader_dao = ReaderDAO(db.session)
reader_service = ReaderService(reader_dao)

author_dao = AuthorDAO(db.session)
author_service = AuthorService(author_dao)

book_dao = BookDAO(db.session)
books_service = BookService(book_dao, author_service, reader_service)

user_dao = UserDAO(db.session)
user_service = UserService(user_dao, reader_service, books_service)

auth_service = AuthService(user_service)

news_dao = NewsDAO(db.session)
comment_dao = CommentDAO(db.session)

news_service = NewsService(news_dao, user_service, comment_dao)
comment_service = CommentService(comment_dao, news_service, user_service)
