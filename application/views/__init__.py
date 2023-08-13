__all__ = [
    'auth_ns',
    'author_ns',
    'book_ns',
    'comment_ns',
    'news_ns',
    'reader_ns',
    'user_ns',
]

from .auth_views import auth_ns
from .authors_views import author_ns
from .books_views import book_ns
from .comments_views import comment_ns
from .news_views import news_ns
from .readers_views import reader_ns
from .users_views import user_ns
