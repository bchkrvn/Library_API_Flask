from dao.base_dao import BaseDAO
from dao.models.models_dao import Reader


class ReaderDAO(BaseDAO):
    """
    DAO для работы с читателями
    """
    __model__ = Reader
