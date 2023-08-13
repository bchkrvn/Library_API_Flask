__all__ = [
    'AuthPostSchema',
    'AuthPutSchema',
    'AuthorSchema',
    'AuthorPutSchema',
    'BookSchema',
    'BookTransferSchema',
    'BookPatchSchema',
    'CommentsSchema',
    'NewsValidateSchema',
    'ReaderSchema',
    'UserSchema',
    'UserPasswordSchema',
]

from .auth_schemas import AuthPostSchema, AuthPutSchema
from .authors_schemas import AuthorSchema, AuthorPutSchema
from .books_shemas import BookSchema, BookTransferSchema, BookPatchSchema
from .comments_schema import CommentsSchema
from .news_schema import NewsValidateSchema
from .readers_schemas import ReaderSchema
from .user_schemas import UserSchema, UserPasswordSchema
