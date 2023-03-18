from dao.base_dao import BaseDAO
from dao.models.models_dao import Author


class AuthorDAO(BaseDAO):
    __model__ = Author

    def __init__(self, session):
        super().__init__(session=session)