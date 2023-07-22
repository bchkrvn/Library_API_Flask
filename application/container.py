from .dao.authors_dao import AuthorDAO
from .dao.books_dao import BookDAO
from .dao.comment_dao import CommentDAO
from .dao.news_dao import NewsDAO
from .dao.readers_dao import ReaderDAO
from .dao.users_dao import UserDAO
from .services.authors_service import AuthorService
from .services.auths_service import AuthService
from .services.books_service import BookService
from .services.comment_service import CommentService
from .services.news_service import NewsService
from .services.readers_service import ReaderService
from .services.users_service import UserService
from .setup_db import db

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
