from dao import BaseDAO
from models import Reader


class ReaderDAO(BaseDAO):
    """
    DAO для работы с читателями
    """
    __model__ = Reader
