from dao import AuthorDAO, BookDAO, CommentDAO, NewsDAO, ReaderDAO, UserDAO
from services import AuthorService, AuthService, BookService, CommentService, NewsService, ReaderService, UserService
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
